"""
Functions related to the cache (cache.db)
"""

import asyncio
import hashlib
import logging
import random
import shutil
import time
from collections.abc import Awaitable
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, ParamSpec
from weakref import WeakValueDictionary

from aiohttp import web

from raphson_mp import db, settings

log = logging.getLogger(__name__)

HOUR = 60 * 60
DAY = 24 * HOUR
WEEK = 7 * DAY
MONTH = 30 * DAY
HALFYEAR = 6 * MONTH
YEAR = 12 * MONTH

# Files larger than this size will be stored in external files. Can be changed without affecting existing cache.
EXTERNAL_SIZE = 10 * 1024 * 1024

LOCKS: WeakValueDictionary[str, asyncio.Lock] = WeakValueDictionary()


def _external_path(name: str) -> Path:
    dir = Path(settings.data_dir, "cache")
    dir.mkdir(exist_ok=True)
    return dir / name


async def store(key: str, data: bytes | Path, duration: int) -> None:
    """
    Args:
        key: Cache key
        data: Data to cache
        duration: Suggested cache duration in seconds. Cache duration is varied by up to 25%, to
                  avoid high load when cache entries all expire at roughly the same time.
    """
    log.debug("storing in cache: %s", key)

    # Vary cache duration so cached data doesn't expire all at once
    duration += random.randint(-duration // 4, duration // 4)

    external = False
    if isinstance(data, Path):
        if data.stat().st_size > EXTERNAL_SIZE:
            file_name = hashlib.blake2s(key.encode()).hexdigest()
            external_path = _external_path(file_name)
            log.info("copy %s to external cache file: %s", data.as_posix(), external_path)
            shutil.copyfile(data, external_path)
            data = file_name.encode()  # cached data becomes file name
            external = True
        else:
            data = data.read_bytes()
    else:
        if len(data) > EXTERNAL_SIZE:
            file_name = hashlib.blake2s(key.encode()).hexdigest()
            external_path = _external_path(file_name)
            log.info("write data to external file: %s", external_path)
            _external_path(file_name).write_bytes(data)
            data = file_name.encode()  # cached data becomes file name
            external = True

    expire_time = int(time.time()) + duration

    def thread():
        with db.cache() as conn:
            conn.execute(
                """
                INSERT INTO cache (key, data, expire_time, external)
                VALUES (?, ?, ?, ?)
                """,
                (key, data, expire_time, external),
            )

    await asyncio.to_thread(thread)


async def retrieve(key: str) -> bytes | None:
    """
    Retrieve object from cache
    Args:
        key: Cache key
        partial: Return partial data in the specified range (start, length)
        return_expired: Whether to return the object from cache even when expired, but not cleaned
                        up yet. Should be set to False for short lived cache objects.
    """

    with db.cache(read_only=True) as conn:
        row = conn.execute("SELECT data, external FROM cache WHERE key=?", (key,)).fetchone()

    if row is None:
        log.debug("not cached: %s", key)
        return None

    data, external = row

    # Allow reading external cache files using standard retrieve(), but
    # since these files may be larger than memory, other methods should
    # be preferred instead.
    if external:
        external_path = _external_path(data.decode())
        log.warning("reading large external file into memory: %s", external_path.as_posix())
        data = external_path.read_bytes()

    log.debug("retrieved from cache: %s", key)
    return data


async def retrieve_response(key: str, content_type: str) -> web.StreamResponse | None:
    with db.cache(read_only=True) as conn:
        row = conn.execute("SELECT data, external FROM cache WHERE key=?", (key,)).fetchone()

    if row is None:
        return None

    data, external = row

    if external:
        log.info("returning FileResponse directly")
        external_path = _external_path(data.decode())
        return web.FileResponse(external_path)

    log.info("not an external file, returning full data in response")
    return web.Response(body=data, content_type=content_type)


@dataclass
class CacheData:
    data: bytes
    duration: int


P = ParamSpec("P")


async def retrieve_or_store(
    key: str, data_func: Callable[P, Awaitable[CacheData]], *args: P.args, **kwargs: P.kwargs
) -> bytes:
    lock = LOCKS.get(key, asyncio.Lock())
    LOCKS[key] = lock

    # Some clients make repeated requests to a cached resource, aborting the request just before
    # the resource has been written to the cache. Use shield() to prevent this.

    async def never_cancelled():
        async with lock:
            data = await retrieve(key)
            if data is not None:
                return data
            cache = await data_func(*args, **kwargs)
            await store(key, cache.data, cache.duration)
            return cache.data

    return await asyncio.shield(never_cancelled())


async def cleanup() -> None:
    """
    Remove any cache entries that are beyond their expire time.
    """

    def thread():
        with db.cache() as conn:
            # TODO clean up external cache entries
            count = conn.execute(
                "DELETE FROM cache WHERE expire_time < ? AND external = false", (int(time.time()),)
            ).rowcount
            # The number of vacuumed pages is limited to prevent this function
            # from blocking for too long. Max 65536 pages = 256MiB
            # For an unknown reason, incremental_vacuum only works in executescript(), not regular execute()
            conn.executescript("PRAGMA incremental_vacuum(65536)")
            log.info("Deleted %s entries from cache", count)

    await asyncio.to_thread(thread)

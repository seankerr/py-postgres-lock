"""
Lock support for asyncpg.
"""

from .lock import Lock


def acquire(lock: Lock, block: bool = True) -> bool:
    """
    This function is not implemented.

    Parameters:
        lock (Lock): Lock.
        block (bool): Return only once the lock has been acquired.

    Returns:
        bool: True, if the lock was acquired, otherwise False.

    Raises:
        NotImplementedError: This function is not implemented.
    """
    raise NotImplementedError("ascynpg interface does not support acquire()")


async def acquire_async(lock: Lock, block: bool = True) -> bool:
    """
    Acquire the lock asynchronously.

    Parameters:
        lock (Lock): Lock.
        block (bool): Return only once the lock has been acquired.

    Returns:
        bool: True, if the lock was acquired, otherwise False.
    """
    lock_func = lock.blocking_lock_func

    if not block:
        lock_func = lock.nonblocking_lock_func

    result = await lock.conn.fetchval(f"SELECT pg_catalog.{lock_func}({lock.lock_id})")

    # lock function returns True/False in unblocking mode, and always None if in blocking mode
    return False if result is False else True


def release(lock: Lock) -> None:
    """
    This function is not implemented.

    Parameters:
        lock (Lock): Lock.

    Raises:
        NotImplementedError: This function is not implemented.
    """
    raise NotImplementedError("ascynpg interface does not support release()")


async def release_async(lock: Lock) -> None:
    """
    Release the lock asynchronously.

    Parameters:
        lock (Lock): Lock.
    """
    await lock.conn.execute(f"SELECT pg_catalog.{lock.unlock_func}({lock.lock_id})")

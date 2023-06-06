## postgres-lock

Lock mechanism implemented with Postgres advisory locks.

Easily implement distributed database locking.

### Install

```sh
pip install postgres-lock
```

### Supported database interfaces

- **asyncpg**
  - asynchronous
- **psycopg2**
  - synchronous
- **psycopg3**
  - asynchronous
  - synchronous
- **sqlalchemy** (supports version 1 & 2; can use any underlying database interface)
  - asynchronous
  - synchronous

### Why would I use this?

- Postgres table locks aren't sufficient for your use-case
- Postgres row locks don't work on `INSERT`
- You want to prevent race conditions between `INSERT` and `UPDATE` on the same primary key
- None of the aforementioned details fit your use-case, but you have Postgres installed and need to prevent race conditions in a distributed system

### Default operation

By default `postgres-lock` will use `session` lock scope in `blocking` mode with
`rollback_on_error` enabled. The `session` lock scope means only a single database connection can
acquire the lock at a time.

### Usage

All work revolves around the `Lock` and `AsyncLock` classes.

The easiest way to use `Lock` or `AsyncLock` is with `with` or `async with` statements. The lock
will be released automatically. If `rollback_on_error` is enabled (default), rollbacks are
automatically handled prior to the lock being released.

_Using `with` and `async with` implies blocking mode._

```python
from postgres_lock import Lock

# setup connection
conn = ...

# create and use lock
with Lock(conn, "shared-identifier"):
    # do something here
    pass
```

Now compare the above example to the equivalent try/finally example below:

```python
from postgres_lock import Lock

# setup connection
conn = ...

# create lock
lock = Lock(conn, "shared-identifier")

try:
    # acquire lock
    lock.acquire()

    try:
        # do something here
        pass

    except Exception as exc:
        # handle_error() will rollback the transaction by default
        lock.handle_error(exc)

        raise exc
finally:
    # release lock (this is safe to run even if the lock has not been acquired)
    lock.release()
```

### Asynchronous usage (without `async with`)

```python
from postgres_lock import AsyncLock

# setup connection
conn = ...

# create lock
lock = AsyncLock(conn, "shared-identifier")

try:
    # acquire lock
    await lock.acquire()

    try:
        # do something here
        pass

    except Exception as exc:
        # handle_error() will rollback the transaction by default
        await lock.handle_error(exc)

        raise exc
finally:
    # release lock (this is safe to run even if the lock has not been acquired)
    await lock.release()
```

### Non-blocking mode (supports async as well)

```python
from postgres_lock import Lock

# setup connection
conn = ...

# create lock
lock = Lock(conn, "shared-identifier")

# acquire lock
if lock.acquire(block=False):
    # do something here
    pass

else:
    # could not acquire lock
    pass

# release lock (this is safe to run even if the lock has not been acquired)
lock.release()
```

### Specify the database interface manually

```python
from postgres_lock import Lock

# setup connection
conn = ...

# create
lock = Lock(conn, "shared-identifier", interface="sqlalchemy")

# do things with the lock
```

### Handle rollbacks manually

```python
from postgres_lock import Lock

# setup connection
conn = ...

# create and use lock
lock = Lock(conn, "shared-identifier", rollback_on_error=False)

# do things with the lock
```

### Changelog

- **0.1.3**
  - Add AsyncLock and rename \*\_async() so they match the Lock methods
- **0.1.2**
  - Add Lock.rollback_on_error (default true)
  - Add Lock.handle_error() & Lock.handle_error_async()
- **0.1.1**
  - Key can be str or int

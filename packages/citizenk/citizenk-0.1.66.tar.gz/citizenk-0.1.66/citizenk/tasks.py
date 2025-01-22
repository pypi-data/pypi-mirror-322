# Code Adapted/Copied From fastapi_utils
# https://github.com/dmontagu/fastapi-utils/blob/master/fastapi_utils/tasks.py

from __future__ import annotations

import asyncio
import logging
from asyncio import ensure_future
from datetime import datetime
from functools import wraps
from traceback import format_exception
from typing import Callable

from croniter import croniter

from .utils import CitizenKError


def repeat_every(
    *,
    seconds: float,
    wait_first: bool = False,
    logger: logging.Logger | None = None,
    raise_exceptions: bool = False,
    max_repetitions: int | None = None,
) -> Callable:
    """
    This function returns a decorator that modifies a function so it is periodically re-executed after its first call.
    The function it decorates should accept no arguments and return nothing. If necessary, this can be accomplished
    by using `functools.partial` or otherwise wrapping the target function prior to decoration.

    Parameters
    ----------
    seconds: float
        The number of seconds to wait between repeated calls
    wait_first: bool (default False)
        If True, the function will wait for a single period before the first call
    logger: Optional[logging.Logger] (default None)
        The logger to use to log any exceptions raised by calls to the decorated function.
        If not provided, exceptions will not be logged by this function (though they may be handled by the event loop).
    raise_exceptions: bool (default False)
        If True, errors raised by the decorated function will be raised to the event loop's exception handler.
        Note that if an error is raised, the repeated execution will stop.
        Otherwise, exceptions are just logged and the execution continues to repeat.
        See https://docs.python.org/3/library/asyncio-eventloop.html#asyncio.loop.set_exception_handler for more info.
    max_repetitions: Optional[int] (default None)
        The maximum number of times to call the repeated function. If `None`, the function is repeated forever.
    """

    def decorator(func):
        """
        Converts the decorated function into a repeated, periodically-called version of itself.
        """
        if not asyncio.iscoroutinefunction(func):
            raise CitizenKError("repeat_every callable must be async")

        @wraps(func)
        async def wrapped() -> None:
            repetitions = 0

            async def loop() -> None:
                nonlocal repetitions
                if wait_first:
                    await asyncio.sleep(seconds)
                while max_repetitions is None or repetitions < max_repetitions:
                    try:
                        await func()  # type: ignore
                        repetitions += 1
                    except Exception as exc:
                        if logger is not None:
                            formatted_exception = "".join(
                                format_exception(type(exc), exc, exc.__traceback__)
                            )
                            logger.error(formatted_exception)
                        if raise_exceptions:
                            raise exc
                    await asyncio.sleep(seconds)

            ensure_future(loop())

        return wrapped

    return decorator


def get_delta(cron):
    """
    This function returns the time delta between now and the next cron execution time.
    """
    now = datetime.now()
    cron = croniter(cron, now)
    return (cron.get_next(datetime) - now).total_seconds()


def repeat_at(
    *,
    cron: str,
    logger: logging.Logger = None,
    raise_exceptions: bool = False,
    max_repetitions: int = None,
) -> Callable:
    """
    This function returns a decorator that makes a function execute periodically as per the cron expression provided.

    :: Params ::
    ------------
    cron: str
        Cron-style string for periodic execution, eg. '0 0 * * *' every midnight
    logger: logging.Logger (default None)
        Logger object to log exceptions
    raise_exceptions: bool (default False)
        Whether to raise exceptions or log them
    max_repetitions: int (default None)
        Maximum number of times to repeat the function. If None, repeat indefinitely.

    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            repetitions = 0
            if not croniter.is_valid(cron):
                raise ValueError(f"Invalid cron expression: '{cron}'")

            async def loop(*args, **kwargs):
                nonlocal repetitions
                while max_repetitions is None or repetitions < max_repetitions:
                    try:
                        sleep_time = get_delta(cron)
                        await asyncio.sleep(sleep_time)
                        await func(*args, **kwargs)
                    except Exception as e:
                        if logger is not None:
                            logger.exception(e)
                        if raise_exceptions:
                            raise e
                    repetitions += 1

            ensure_future(loop(*args, **kwargs))

        return wrapper

    return decorator

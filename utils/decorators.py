import logging
import time
from functools import wraps
from typing import Callable, ParamSpec, TypeVar
logger = logging.getLogger(__name__)


P= ParamSpec("P")
T = TypeVar("T")


def title (func:Callable[P, T])->Callable[P, T]:
    @wraps(func)
    def wrap(*args:P.args, **kwargs:P.kwargs)->T:

        logger.debug("شروع فرایند دکوریتور تیتر")

        print("َشروع عملیات کتابخانه")
        result=func(*args, **kwargs)

        logger.debug("پایان فرایند دکوریتور تیتر")

        print("پایان عملیات کتابخانه")
        return result
    return wrap



def timer(func: Callable[P, T]) -> Callable[P, T]:
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:

        logger.debug("شروع اجرای دکوریتور timer")

        start = time.perf_counter()

        try:
            return func(*args, **kwargs)

        finally:
            end = time.perf_counter()
            elapsed = end - start

            logger.info(
                f"زمان اجرای تابع {func.__name__}: "
                f"{elapsed:.6f} ثانیه"
            )

            logger.debug("پایان اجرای دکوریتور timer")

            print(
                f"زمان اجرا: {elapsed:.6f} ثانیه"
            )

    return wrapper
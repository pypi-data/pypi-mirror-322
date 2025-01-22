import logging

from functools import wraps



logger = logging.getLogger(__name__)


class x2TException:
    @staticmethod
    def handler(log: bool = True):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if log:
                        logger.error(
                            f"An error occurred in {func.__name__} "
                            f"with args={args}, kwargs={kwargs}: {str(e)}",
                            exc_info=True,
                        )
                    return {"error": str(e), "status": "failed"}
            return wrapper
        return decorator

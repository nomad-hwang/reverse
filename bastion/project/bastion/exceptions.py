# Handle exceptions for the bastion project
# decorators.py
import logging
from functools import wraps

from fastapi import HTTPException, status

LOGGER = logging.getLogger(__name__)


def handle_http_exception(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if hasattr(e, "status_code") and hasattr(e, "detail"):
                raise HTTPException(status_code=e.status_code, detail=e.detail)
            logging.exception(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error",
            )

    return wrapper

"""
Error handler middleware for consistent error formatting.
"""

import logging
from typing import Callable
from fastapi import Request, Response, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from sqlalchemy.exc import SQLAlchemyError

from app.exceptions import AppException, NotFoundError, ValidationError

logger = logging.getLogger(__name__)


class ErrorHandlerMiddleware:
    """
    Middleware to capture and format errors consistently.
    """

    async def __call__(self, request: Request, call_next: Callable) -> Response:
        """
        Process request and handle errors.
        
        Args:
            request: FastAPI Request
            call_next: Next middleware/route handler
        
        Returns:
            Response with formatted error if exception occurred
        """
        try:
            response = await call_next(request)
            return response
        except RequestValidationError as e:
            # Pydantic validation errors
            logger.warning(f"Validation error: {e.errors()}")
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"detail": e.errors()},
            )
        except StarletteHTTPException as e:
            # HTTP exceptions (404, etc.)
            logger.warning(f"HTTP exception: {e.status_code} - {e.detail}")
            return JSONResponse(
                status_code=e.status_code,
                content={"detail": e.detail},
            )
        except ValidationError as e:
            # Application validation errors
            logger.warning(f"Validation error: {e.message}")
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"detail": e.message},
            )
        except NotFoundError as e:
            # Resource not found errors
            logger.warning(f"Not found error: {e.message}")
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"detail": e.message},
            )
        except AppException as e:
            # Other application errors
            logger.error(f"Application error: {e.message}")
            return JSONResponse(
                status_code=e.status_code,
                content={"detail": e.message},
            )
        except SQLAlchemyError as e:
            # Database errors
            logger.error(f"Database error: {str(e)}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"detail": "Database error occurred"},
            )
        except Exception as e:
            # Unexpected errors
            logger.exception(f"Unexpected error: {str(e)}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"detail": "Internal server error"},
            )


# Create middleware instance
error_handler_middleware = ErrorHandlerMiddleware()


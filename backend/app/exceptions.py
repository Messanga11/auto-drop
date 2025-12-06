from fastapi import HTTPException, status
from typing import Any, Dict, Optional


class AppException(Exception):
    """Base application exception"""
    def __init__(self, message: str, status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class NotFoundError(AppException):
    """Resource not found exception"""
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, status_code=status.HTTP_404_NOT_FOUND)


class ValidationError(AppException):
    """Validation error exception"""
    def __init__(self, message: str = "Validation error"):
        super().__init__(message, status_code=status.HTTP_400_BAD_REQUEST)


class ExternalAPIError(AppException):
    """External API error exception"""
    def __init__(self, message: str = "External API error", status_code: int = status.HTTP_502_BAD_GATEWAY):
        super().__init__(message, status_code)


async def exception_handler(request, exc: AppException):
    """Global exception handler"""
    return {
        "error": exc.message,
        "status_code": exc.status_code
    }


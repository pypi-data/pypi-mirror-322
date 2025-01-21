from fastapi import HTTPException
from inneed_utility_service.enums.enums import ResponseType
from inneed_utility_service.fast_api.response_helpers import generate_error_response

class DatabaseError(Exception):
    """Generic exception for database-related errors."""
    pass

def handle_exception(e: Exception) -> HTTPException:
    """
    Handle different types of exceptions and generate appropriate error responses.

    Args:
        e (Exception): The exception to handle.

    Returns:
        HTTPException: The corresponding error response based on the exception type.
    """
    if isinstance(e, DatabaseError):
        print(f"Database error: {e}")
        return generate_error_response(
            error_type=ResponseType.INTERNAL_SERVER_ERROR,
            details=f"Database error occurred: {str(e)}"
        )
    elif isinstance(e, ValueError):
        print(f"Value error: {e}")
        return generate_error_response(
            error_type=ResponseType.VALIDATION_ERROR,
            details=f"Invalid input: {str(e)}"
        )
    else:
        print(f"Unexpected error: {e}")
        return generate_error_response(
            error_type=ResponseType.INTERNAL_SERVER_ERROR,
            details="An unexpected error occurred. Please try again later."
        )

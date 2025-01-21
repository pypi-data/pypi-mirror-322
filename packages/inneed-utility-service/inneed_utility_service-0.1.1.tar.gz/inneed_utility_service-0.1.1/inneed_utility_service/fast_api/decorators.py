from functools import wraps
from fastapi import HTTPException, Request

def validate_token_header(expected_token: str):
    """
    Decorator to validate the Authorization header with a configurable token.
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            token = request.headers.get("Authorization")
            if not token or token != f"Bearer {expected_token}":
                raise HTTPException(status_code=401, detail="Invalid token")
            return await func(request, *args, **kwargs)
        return wrapper
    return decorator

from functools import wraps
from typing import Callable, List, Union

response_403 = {
    "errorType": "Unauthorized",
    "message": "Invalid identity claims",
    "statusCode": 403,
}


def role_required(required_roles: Union[str, List[str]]):
    """
    Decorator and standalone function to check if the current user has any of the required roles.

    If used as a decorator, returns an AppSync-compatible 403 response on failure.
    If used as a direct function, returns a boolean.

    Args:
        required_roles (Union[str, List[str]]): The role(s) required to access the resource.

    Returns:
        Callable: Decorator or standalone function.
    """
    # Normalize required_roles to a list
    if isinstance(required_roles, str):
        required_roles = [required_roles]

    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Extract the first argument, assuming it's the AppSync event
            event = kwargs.get("event", args[0] if args else None)
            if not event or "identity" not in event or "claims" not in event["identity"]:
                return response_403

            # Get the roles from claims
            claims = event["identity"]["claims"]
            user_roles = claims.get("roles", [])

            # Check if any of the required roles are in the user's roles
            if not any(role in user_roles for role in required_roles):
                return response_403

            # Proceed with the wrapped function
            return func(*args, **kwargs)

        return wrapper

    def standalone(event: dict) -> bool:
        """Direct function to check role without using as a decorator."""
        if not event or "identity" not in event or "claims" not in event["identity"]:
            return False

        claims = event["identity"]["claims"]
        user_roles = claims.get("roles", [])
        return any(role in user_roles for role in required_roles)

    # Return the decorator or standalone function
    return decorator if callable else standalone

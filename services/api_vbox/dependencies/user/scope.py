"""All scopes dependencies.

Create your Scope dependencies by inheriting base class VerifyScope.
Used as a FastAPI dependency.

@author Rxinui
"""
from abc import ABC
from enumerations import Scope
from fastapi import Request, HTTPException, status


class VerifyScope(ABC):
    """Base class to define Scope dependency."""

    def __init__(self, request: Request, *scopes: Scope):
        """Verify user scope to check his access right before processing his request.

        Args:
            request (Request): request emitted

        Raises:
            HTTPException: User not authenticated
            HTTPException: User does not have right scope

        Returns:
            Request: request
        """
        if not getattr(request.state, "token_payload", None):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unauthorized access. Missing token payload. Must be authenticated first.",
            )
        scopes_valid = all(
            s.value not in request.state.token_payload["scope"] for s in scopes
        )
        if scopes_valid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User does not have the right scope.",
            )


class ReadScope(VerifyScope):
    """User scope to read VMs"""

    def __init__(self, request: Request):
        super().__init__(request, Scope.READ, Scope.ALL)

class CreateScope(VerifyScope):
    """User scope to create VMs"""

    def __init__(self, request: Request):
        super().__init__(request, Scope.CREATE, Scope.ALL)

class ControlScope(VerifyScope):
    """User scope to create VMs"""

    def __init__(self, request: Request):
        super().__init__(request, Scope.CONTROL, Scope.ALL)

"""All Authentication strategies.

Create your Authentication strategy here by inheriting base class AuthStrategy.
The strategy is used as a FastAPI dependency.

@author Rxinui
"""
import os
import httpx
from utils import logger
from fastapi import Header, status, HTTPException, Request
from enumerations import Scope

logger = logger(__name__, "main.py.log")


class HTTPBearerTokenAuth:
    """HTTP Bearer Token strategy.

    Verify the Bearer token within HTTP Authorization header.
    Extract the jwt token and add it as 'token_payload' if the token
    is legitimate.
    """

    @staticmethod
    def __verify(request: Request, response):
        if response.status_code == status.HTTP_401_UNAUTHORIZED:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unauthorized access. Missing or invalid token.",
            )
        request.state.token_payload = response.json()
        logger.info("authenticated user id: %s", request.state.token_payload["sub"])

    def __init__(self, request: Request, authorization: str = Header(default=None)):
        """ "Requires 'Authorization' header to proceed.

        Will check the validity of the authentication token.
        If the validity of the token is approved, then the token data will
        be assigned to the request.state attributes.

        Args:
            request (Request): emitted request
            authorization (str): HTTP Authorization header

        Raises:
            HTTPException: Unauthorized access.

        Returns:
            Request: updated request with 'token_payload'
        """
        if not authorization:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unauthorized access. Missing 'Authorization' header.",
            )
        with httpx.Client(
            base_url=os.getenv("API_AUTH_URL"), headers={"Authorization": authorization}
        ) as api_auth:
            response = api_auth.get("/token/internal/verify")
            logger.info("authentication on 'api_auth' is %s.", response.reason_phrase)
            self.__verify(request, response)

    async def asynchrone(self, request: Request, authorization: str = Header(...)):
        """Async version of HTTP Bearer Token Auth.

        Args:
            request (Request): emitted request
            authorization (str): HTTP Authorization header

        Raises:
            HTTPException: Unauthorized access.

        Returns:
            Request: updated request with 'token_payload'
        """
        if not authorization:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unauthorized access. Missing 'Authorization' header.",
            )
        async with httpx.AsyncClient(
            base_url=os.getenv("API_AUTH_URL"), headers={"Authorization": authorization}
        ) as api_auth:
            response = api_auth.get("/token/internal/verify")
            logger.info("authentication on 'api_auth' is %s.", response.reason_phrase)
            self.__verify(request, response)

class NoAuth:

    def __init__(self, request: Request, authorization: str = Header(default=None)):
        """ "Requires 'Authorization' header to proceed.

        Will check the validity of the authentication token.
        If the validity of the token is approved, then the token data will
        be assigned to the request.state attributes.

        Args:
            request (Request): emitted request
            authorization (str): HTTP Authorization header

        Raises:
            HTTPException: Unauthorized access.

        Returns:
            Request: updated request with 'token_payload'
        """
        request.state.token_payload = {"sub": "noauth.guest", "scope": Scope.ALL.value}


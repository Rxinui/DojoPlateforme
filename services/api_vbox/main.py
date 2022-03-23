"""API vbox powered with Python and FastAPI.

@author Rxinui
@date 2022-01-21
@see https://www.virtualbox.org/manual/ch08.html
"""

import os
import json
from re import A
import subprocess
import uuid
import httpx
from typing import List, Optional, Union, Tuple, Any
from models import BasicResponse, BasicError
from fastapi import FastAPI, Query, status, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.openapi.utils import get_openapi
from starlette.exceptions import HTTPException as StarletteHTTPException
from openapi import api_vbox_openapi
from dotenv import load_dotenv
from rabbitmq.rpc import RPCClient
from vboxmanage import VBoxManageBuilder
from lib import get_logger, DEBUG

load_dotenv()

EXECMODE_CONTAINER = "container"
EXECMODE_LOCAL = "local"
logger = get_logger(__name__, f"{__file__}.log", level=DEBUG)
app = FastAPI()
app_users = {}

# TODO implement a Token Bearer check before executing request
def _openapi():
    """Update openAPI with custom values stored in openapi/.

    Returns:
        Dict[str,Any]: openAPI schema
    """
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="API vbox",
        version="0.1",
        description="OpenAPI of API vbox",
        servers=[{"url": "https://localhost:8000/", "description": "API dev server"}],
        routes=app.routes,
    )
    app.openapi_schema = api_vbox_openapi(openapi_schema)
    return app.openapi_schema


app.openapi = _openapi


def _get_user_rpc_client(user: Any) -> Union[str, RPCClient]:
    if isinstance(user, Request):
        return app_users[user.client.host].get("rpc")
    raise ValueError("Incorrect user within main.app")


def _get_user_id(user: Any) -> Union[str, None]:
    if isinstance(user, Request):
        return app_users[user.client.host].get("user_id")
    raise ValueError("Incorrect user within main.app")


def _set_user_rpc_client(user: Any):
    if isinstance(user, Request):
        data = app_users.setdefault(user.client.host, {})
        if not data.get("rpc"):
            data["rpc"] = RPCClient(
                _get_user_id(user), os.getenv("API_VBOX_USERS_REQUEST_QUEUE")
            )
        return data["rpc"]
    raise ValueError("Incorrect user within main.app")


def _set_user_id(user: Any):
    if isinstance(user, Request):
        if user.client.host not in app_users:
            app_users[user.client.host] = {"user_id": str(uuid.uuid4())}
    else:
        raise ValueError("Incorrect user within main.app")


@app.exception_handler(status.HTTP_401_UNAUTHORIZED)
@app.middleware("http")
async def verify_authentication(request: Request, call_next):
    print(request.headers["Authorization"])
    token_bearer = request.headers["Authorization"]
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{os.getenv('API_AUTH_URL')}/token/internal/verify",
            headers={"Authorization": token_bearer},
        )
        print("debug:verify:", response)
        if response.status_code == status.HTTP_401_UNAUTHORIZED:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content=BasicError(
                    code="AUTH_FAILED",
                    error="Token bearer not valid.",
                    details="api_auth rejected your request.",
                ).__dict__,
            )
        token_payload = response.json()
        return await call_next(request)


@app.exception_handler(StarletteHTTPException)
async def __http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content=BasicError(
            code="BAD_HTTP_VALIDATION",
            error="HTTP Error",
            details=str(exc.detail),
        ).__dict__,
    )


@app.exception_handler(RequestValidationError)
async def __validation_exception_handler(request, exc):
    """Validation exception handler"""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=BasicError(
            code="BAD_REQUEST_VALIDATION",
            error="Error during HTTP arguments validation",
            details=exc.errors(),
        ).__dict__,
    )


def _execute_cmd(user: Request, cmd: List[str]) -> str:
    """Execute a shell command.

    Args:
        cmd (List[str]): command

    Returns:
        str: command output
    """
    # see also: subprocess.check_output(cmd).decode("utf-8")
    if os.environ["API_VBOX_EXECMODE"] == EXECMODE_CONTAINER:
        _set_user_rpc_client(user)
        rpc = _get_user_rpc_client(user)
        response = rpc.send_request({"cmd": cmd})
        output = response["res"]["output"]
    elif os.environ["API_VBOX_EXECMODE"] == EXECMODE_LOCAL:
        with subprocess.Popen(cmd, stdout=subprocess.PIPE) as proc:
            output = proc.communicate()[0].decode("utf-8")
    else:
        raise EnvironmentError("API_VBOX_EXECMODE env variable is missing.")
    print("debug:app_users:", app_users)
    return output


@app.get(
    "/list",
    response_model=BasicResponse,
    status_code=status.HTTP_202_ACCEPTED,
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": BasicError},
        status.HTTP_401_UNAUTHORIZED: {"model": BasicError},
        status.HTTP_403_FORBIDDEN: {"model": BasicError},
        status.HTTP_404_NOT_FOUND: {"model": BasicError},
        status.HTTP_406_NOT_ACCEPTABLE: {"model": BasicError},
        status.HTTP_429_TOO_MANY_REQUESTS: {"model": BasicError},
    },
)
async def vbox_manage_list(
    request: Request,
    q: str = Query(
        ...,
        regex=VBoxManageBuilder.list().parser.get_directives_regex(),
        max_length=98,
        min_length=3,
    ),
    sort: Optional[bool] = False,
    long: Optional[bool] = False,
):
    """
    Apply `VBoxManage list <directive>` according to {list} q parameter.

    Args:
        list (Optional[Query[List[str]]]): q to list

    Returns:
        (BasicResponse): /list result
    """

    def get_list_directive_cmd(directive: str, **kwargs) -> Union[None, str]:
        """
        Check validity of a given directive.

        Returns either the VBoxManage list command or
        None if the directive is incorrect.
        """
        try:
            return getattr(VBoxManageBuilder.list(), directive)(**kwargs)
        except AttributeError as exc:
            logger.warning(
                "%s directive=%s is a bad directive.",
                app.url_path_for("vbox_manage_list"),
                directive,
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"'{directive}' is not a list directive.",
            ) from exc

    def process_list_directive(
        directive: str, **kwargs
    ) -> Tuple[Union[None, str], Any]:
        """
        Process a directive passed by q and parse the result.

        Looks up the directive sent if exist then execute it.
        The following output will be parsed and return.
        """
        cmd = get_list_directive_cmd(directive, **kwargs)
        if not cmd:
            return None, "Incorrect list directive."
        output = _execute_cmd(request, cmd)
        f_parse = getattr(VBoxManageBuilder.list().parser, f"parse_{directive}")
        res = f_parse(output, kwargs["long"])
        return directive, res

    if not q:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": "MISSING_LIST_QUERY",
                "msg": "Missing query to directive list.",
            },
        )
    _set_user_id(request)
    items = {}
    items["sort"] = sort
    items["long"] = long
    logger.info("%s sort=%s long=%s.", app.url_path_for("vbox_manage_list"), sort, long)
    q = q.split(",")
    for directive in q:
        valid_directive, parsed = process_list_directive(
            directive, sort=sort, long=long
        )
        items[valid_directive] = parsed
        logger.info(
            "%s directive=%s parsed.", app.url_path_for("vbox_manage_list"), directive
        )
    return BasicResponse(msg="/list", items=items)


@app.on_event("shutdown")
def shutdown_event():
    """
    Save new openapi schema.
    """
    with open("./openapi/openapi.json", "w", encoding="utf-8") as fo:
        json.dump(app.openapi(), fo, indent=2)

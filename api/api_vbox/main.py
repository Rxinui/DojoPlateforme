"""API vbox powered with Python and FastAPI.

@author Rxinui
@date 2022-01-21
@see https://www.virtualbox.org/manual/ch08.html
"""

import json
import subprocess
from typing import List, Optional, Union, Tuple, Any
from models import BasicResponse, BasicError
from fastapi import FastAPI, Query, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.openapi.utils import get_openapi
from openapi import api_vbox_openapi
from vboxmanage import VBoxManageBuilder
from lib import get_logger, DEBUG

logger = get_logger(__name__, f"{__file__}.log", level=DEBUG)
app = FastAPI()

# TODO implement a Token Bearer check before executing request
# TODO return correct 4XX HTTP response


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


def _execute_cmd(cmd: List[str]) -> str:
    """Execute a shell command.

    Args:
        cmd (List[str]): command

    Returns:
        str: command output
    """
    # see also: check_output()
    # return subprocess.check_output(cmd).decode("utf-8")
    with subprocess.Popen(cmd, stdout=subprocess.PIPE) as proc:
        return proc.communicate()[0].decode("utf-8")


@app.get(
    "/vbox",
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
    q: str = Query(
        ...,
        regex=VBoxManageBuilder.list().parser.get_directives_regex(),
        max_length=98,
        min_length=3
    ),
    sort: Optional[bool] = False,
    long: Optional[bool] = False,
):
    """
    Apply `VBoxManage list <directive>` according to {list} q parameter.

    Args:
        list (Optional[Query[List[str]]]): q to list

    Returns:
        (BasicResponse): /vbox result
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
        output = _execute_cmd(cmd)
        f_parse = getattr(VBoxManageBuilder.list().parser, f"parse_{directive}")
        res = f_parse(output, kwargs["long"])
        return directive, res

    if not q:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=dict(BasicError(msg="Missing query.")),
        )
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
    return BasicResponse(msg="/vbox", items=items)


@app.on_event("shutdown")
def shutdown_event():
    """
    Save new openapi schema.
    """
    with open("./openapi/openapi.json", "w", encoding="utf-8") as fo:
        json.dump(app.openapi(), fo, indent=2)

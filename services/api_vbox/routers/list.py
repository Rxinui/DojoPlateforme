"""FastAPI router to /list.

Enable the use of `VBoxManage list` by HTTP using the api_vbox

@author Rxinui
"""

from typing import Optional, Union, Tuple, Any
from fastapi import APIRouter, Query, status, HTTPException, Request, Depends
from models import BasicResponse, BasicError
from vboxmanage import VBoxManageBuilder
from utils import logger, execute_cmd
from dependencies.user import ReadScope

logger = logger(__name__, "main.py.log")
router = APIRouter(tags=["list"])


def cmd_from_directive(
    directive: str, sort: bool = False, long: bool = False
) -> Union[None, str]:
    """
    Check validity of a given directive.

    Returns either the VBoxManage list command or
    None if the directive is incorrect.
    """
    try:
        return (
            getattr(VBoxManageBuilder.list, directive)
            .apply_options(sort=sort, long=long)
            .build()
        )
    except AttributeError as exc:
        logger.warning(
            "%s directive=%s is a bad directive.",
            router.url_path_for("vbox_manage_list"),
            directive,
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"'{directive}' is not a list directive.",
        ) from exc


def process_list_directive(
    user: Any, directive: str, sort: bool = False, long: bool = False
) -> Tuple[Union[None, str], Any]:
    """
    Process a directive passed by q and parse the result.

    Looks up the directive sent if exist then execute it.
    The following output will be parsed and return.
    """
    cmd = cmd_from_directive(directive, sort, long)
    output, _, _ = execute_cmd(user, cmd)
    f_parse = getattr(VBoxManageBuilder.list.parser, f"parse_{directive}")
    res = f_parse(output, long)
    return directive, res


@router.get(
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
    dependencies=[Depends(ReadScope)],
)
async def vbox_manage_list(
    request: Request,
    q: str = Query(
        ...,
        regex=VBoxManageBuilder.list.parser.get_directives_regex(),
        max_length=98,
        min_length=3,
    ),
    sort: Optional[bool] = False,
    long: Optional[bool] = False,
):
    """
    Apply `VBoxManage list <directive>` with parameter `q` a list of directives.
    """
    if not q:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": "MISSING_LIST_QUERY",
                "msg": "Missing query to directive list.",
            },
        )
    q = q.split(",")
    items = {}
    items["sort"] = sort
    items["long"] = long
    logger.info(
        "endpoint '%s' with sort=%s long=%s q=%s.",
        router.url_path_for("vbox_manage_list"),
        sort,
        long,
        q,
    )
    for directive in q:
        valid_directive, parsed = process_list_directive(
            request.state.token_payload["sub"], directive, sort=sort, long=long
        )
        items[valid_directive] = parsed
    return dict(
        msg=f"success query on {router.url_path_for('vbox_manage_list')}", items=items
    )

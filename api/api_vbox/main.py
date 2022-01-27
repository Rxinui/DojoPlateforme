"""API vbox powered with Python and FastAPI.

@author rly
@date 21/01/2022
@see https://www.virtualbox.org/manual/ch08.html
"""

import subprocess
import logging
from typing import List, Optional, Union, Tuple, Any
from pydantic import BaseModel
from fastapi import FastAPI, Query, status, HTTPException
from vboxmanage import VBoxManageBuilder, VBoxManageListParser

logging.basicConfig(
    filename="./api_vbox.log",
    encoding="utf-8",
    level=logging.DEBUG,
    format="%(asctime)s::%(name)s::%(levelname)s::%(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
)
logger = logging.getLogger(__name__)
app = FastAPI()


class BasicResponse(BaseModel):
    """
    API response model

    msg: message to describe a response
    items: data to submit with the response
    """

    msg: str = ...
    items: dict = {}


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


@app.get("/vbox", response_model=BasicResponse, status_code=status.HTTP_202_ACCEPTED)
async def vbox_manage_list(
    query: Optional[List[str]] = Query([]),
    sort: Optional[bool] = False,
    long: Optional[bool] = False,
):
    """
    Apply `VBoxManage list <directive>` according to {list} query parameter.

    Args:
        list (Optional[Query[List[str]]]): query to list

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
        Process a directive passed by query and parse the result.

        Looks up the directive sent if exist then execute it.
        The following output will be parsed and return.
        """
        cmd = get_list_directive_cmd(directive, **kwargs)
        if not cmd:
            return None, "Incorrect list directive."
        output = _execute_cmd(cmd)
        f_parse = getattr(VBoxManageListParser, f"parse_{directive}")
        res = f_parse(output, kwargs["long"])
        return directive, res

    items = {}
    items["sort"] = sort
    items["long"] = long
    logger.info("%s sort=%s long=%s.", app.url_path_for("vbox_manage_list"), sort, long)
    for directive in query:
        valid_directive, parsed = process_list_directive(
            directive, sort=sort, long=long
        )
        items[valid_directive] = parsed
        logger.info(
            "%s directive=%s parsed.", app.url_path_for("vbox_manage_list"), directive
        )
    return BasicResponse(msg="/vbox", items=items)


@app.get("/vbox/{id_vbox}")
async def get_vbox_by_id(id_vbox: str):
    """
    Apply `VBoxManage showvminfo`.

    Args:
        id_vbox (str): vm id

    Returns:
        (BasicResponse): vm info
    """
    if id_vbox == "1":
        return {"message": f"/vbox/{id_vbox} OK"}
    return

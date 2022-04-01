"""FastAPI router to /import.

Enable the use of `VBoxManage import` by HTTP using the api_vbox

@author Rxinui
"""

from pathlib import Path
from fastapi import APIRouter, status, HTTPException, Request, Depends
from models import BasicResponse, BasicError, OvfSessionParams
from vboxmanage import VBoxManageBuilder
from utils import logger, execute_cmd
from dependencies.user import CreateScope

logger = logger(__name__, "main.py.log")
router = APIRouter(tags=["import"])

VMS_BASEFOLDER = Path("/media/kidr/RDD/vms/")
OVF_BASEFOLDER = Path("/opt/DojoPlateforme/system/virtualbox/ovf/")


@router.post(
    "/import",
    response_model=BasicResponse,
    status_code=status.HTTP_202_ACCEPTED,
    responses={
        status.HTTP_409_CONFLICT: {"model": BasicError},
    },
    dependencies=[Depends(CreateScope)],
)
async def vbox_manage_import(request: Request, ovf_params: OvfSessionParams) -> BasicResponse:
    """Apply `VBoxManage import` command depending on {ovf_params}.

    Args:
        request (Request): request emitted
        ovf_params (OvfSessionParams): ovf parameters

    Raises:
        HTTPException: ovf path {ovf_params.image} does not exist
        HTTPException: error threw during the execution of `VBoxManage import`

    Returns:
        BasicResponse: success response
    """
    ovf_params.image = OVF_BASEFOLDER / ovf_params.image
    if not ovf_params.image.exists():
        logger.error("OVF image '%s' not found", ovf_params.image)
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f"OVF image '{ovf_params.image}' not found",
        )
    ovf_params.image = str(ovf_params.image)
    logger.info("OVF image '%s' is found", ovf_params.image)
    items = {"params": ovf_params}
    cmd = (
        VBoxManageBuilder.import_image.ovf(ovf_params.image)
        .vsys(ovf_params.vsys,basefolder=VMS_BASEFOLDER)
        .vmname(ovf_params.vmname)
        .options(*ovf_params.options)
        .build()
    )
    logger.info("Prepared import command %s", cmd)
    _, error, exit_code = execute_cmd(request.state.token_data["sub"], cmd)
    items.update(VBoxManageBuilder.import_image.parser.parse_result(error, exit_code))
    if exit_code != 0:
        logger.error("Command executed threw an error: %s", items["result"].split("\n"))
        raise HTTPException(status.HTTP_409_CONFLICT, items["result"])
    logger.info("Command executed is a success: %s", items["result"].split("\n"))
    return BasicResponse(
        msg=f"Importation of {ovf_params.image} is a success.", items=items
    )

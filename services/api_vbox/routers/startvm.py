"""FastAPI router to /startvm.

Enable the use of `VBoxManage startvm` by HTTP using the api_vbox

@author Rxinui
"""

from fastapi import APIRouter, status, HTTPException, Request, Depends
from models import BasicResponse, BasicError, StartVMParams
from vboxmanage import VBoxManageBuilder
from dependencies.user import ControlScope
from utils import logger, execute_cmd

logger = logger(__name__, "main.py.log")
router = APIRouter(tags=["startvm"])


@router.post(
    "/startvm",
    response_model=BasicResponse,
    status_code=status.HTTP_202_ACCEPTED,
    responses={
        status.HTTP_409_CONFLICT: {"model": BasicError},
    },
    dependencies=[Depends(ControlScope)]
)
async def vbox_manage_startvm(request: Request, vm_params: StartVMParams) -> BasicResponse:
    """Apply `VBoxManage startvm` command depending on {vm_params}.

    It will start a VM.

    Args:
        request (Request): request emitted
        vm_params (StartVMParams): startvm directive parameters

    Raises:
        HTTPException: vm with given name {vmname} does not exist
        HTTPException: error threw during the execution of `VBoxManage startvm`

    Returns:
        BasicResponse: success response
    """
    cmd = (
        VBoxManageBuilder.startvm.vmname(vm_params.vmname).type(vm_params.type).build()
    )
    logger.info("Preparing startvm command: %s", cmd)
    _, error, exit_code = execute_cmd(request.state.token_data["sub"], cmd)
    if exit_code != 0:
        logger.error("Command executed threw an error: %s", error)
        raise HTTPException(status.HTTP_409_CONFLICT, error)
    logger.info("Startvm command is a success.")
    return BasicResponse(
        msg=f"VM '{vm_params.vmname}' has been started successfully in '{vm_params.type}'.",
        items=vm_params,
    )

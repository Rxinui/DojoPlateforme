"""FastAPI router scenario

@author Rxinui
"""

import os
import json
import time
from base64 import standard_b64decode
from typing import Dict, Any

import httpx
from paramiko import SSHClient, SSHException
from fastapi import APIRouter, status, Request, HTTPException

router = APIRouter(tags=["scenario"])
API_VBOX_URL: str = os.environ["API_VBOX_URL"]
HOST_SSH_PUBKEY: str = os.environ["HOST_SSH_PUBKEY"]
API_VBOX_TIMEOUT_SEC: int = 300  # 5 min
DOJOSENSEI_JSON_DATA_SEP = "@JSON_DATA@\n"
DOJOSENSEI_COMMANDS: dict = {
    "conf_and_start_rport": """
        cd /opt/DojoSensei && \
        ./setup.sh c rport --conf --dojo-userid %s --dojo-workshopid %s && \
        ./setup.sh c rport --start &&  \
        exit $?
    """,
    "conf_ttyd_on_rport": """
        cd /opt/DojoSensei && \
        ./setup.sh c rport --set-ttyd && \
        exit $?
    """,
}

# @router.get("/scenario/test_ssh", status_code=status.HTTP_200_OK)
# async def test_ssh_co(request: Request):
#     ## 3. Connect to VM through SSH
#     with SSHClient() as ssh_client:
#         try:
#             ssh_client.load_system_host_keys()
#             ssh_client.connect("192.168.56.8",username="root")
#             cmd_start_and_configure_rport = """
#             cd /opt/DojoSensei && \
#             ./setup.sh c rport --conf --dojo-userid %s --dojo-workshopid %s && \
#             ./setup.sh c rport --start &&  \
#             ./setup.sh c rport --set-ttyd &&  \
#             exit 0
#             """
#             _ , stdout, stderr = ssh_client.exec_command(cmd_start_and_configure_rport)
#             stdout = stdout.read() + stderr.read()
#             return {"output": stdout}
#         except Exception as exc:
#             print("Error:",exc)
#         return None


INPUT_TEST_1: dict = {
    "training": 1,
    "workshop": 3,
    "imagebox": {
        "rootLogin": "root",
        "filename": "demo_ubuntu_server.ova",
        "type": "VirtualBox",
        "os": "Linux",
        "accessProtocol": "http",
        "options": "",
    },
}


@router.post("/scenario/start_workshop", status_code=status.HTTP_200_OK)
async def scenario_start_workshop(request: Request, params: Dict[str, Any]):
    """[Scenario] Start a workshop.

    "Workshop" is product term to specify "VM environment".

    Scenario:
        1. Create a new instance of .ova image
        2. Start the new instance created
        3. Request rportd the instance's out port
        4. Return the result data

    Returns:
        dict: _description_
    """
    params = INPUT_TEST_1.copy()
    result = {
        "imagebox": {
            "accessUrl": None,
            "accessProtocol": params["imagebox"]["accessProtocol"],
            "boxName": None,
            "stdout": "",
        }
    }
    headers = {"Authorization": request.headers.get("Authorization")}
    _b64padding = "==="
    jwt_payload = standard_b64decode(
        request.headers.get("Authorization").replace("Bearer ", "").split(".")[1]
        + _b64padding
    )
    jwt_payload = json.loads(jwt_payload)
    async with httpx.AsyncClient(
        base_url=API_VBOX_URL, headers=headers, timeout=API_VBOX_TIMEOUT_SEC
    ) as api_vbox:
        import_params = {
            "image": params["imagebox"]["filename"],
            "vmname": f"u{jwt_payload['sub']}w{params['workshop']}",
        }
        result["imagebox"]["boxName"] = import_params["vmname"]
        # 1. Create a new instance of .ova image
        print("Requesting api_vbox:/import...")
        response = await api_vbox.post("/import", json=import_params)
        if response.status_code != status.HTTP_202_ACCEPTED:
            raise HTTPException(status.HTTP_409_CONFLICT, response.json())
        print("Requesting api_vbox:/import successful")
        print(response.json())
        # 2. Start the new instance created
        print("Requesting api_vbox:/startvm...")
        start_params = {"vmname": import_params["vmname"]}
        response = await api_vbox.post("/startvm", json=start_params)
        if response.status_code != status.HTTP_202_ACCEPTED:
            raise HTTPException(status.HTTP_409_CONFLICT, response.json())
        print("Requesting api_vbox:/startvm successful")
        print(response.json())
        # 3. Connect to instance and configure tunnels
        with SSHClient() as ssh_client:
            ssh_client.load_system_host_keys()
            print("Waiting 5 seconds before connecting to workshop...")
            time.sleep(5)
            print("Trying to connect...")
            ssh_client.connect(
                "192.168.56.8",
                username=params["imagebox"]["rootLogin"],
                timeout=100,
                auth_timeout=100,
            )
            cmd_start_and_configure_rport = DOJOSENSEI_COMMANDS.get(
                "conf_and_start_rport"
            ) % (jwt_payload["sub"], params["workshop"])
            # parse --set-ttyd output
            try:
                _, stdout, stderr = ssh_client.exec_command(
                    cmd_start_and_configure_rport
                )
            except SSHException as exc:
                print("Error:command conf_adn_start_rport:", exc)
                raise HTTPException(status.HTTP_409_CONFLICT, str(exc)) from exc
            try:
                result["imagebox"]["stdout"] = stdout.read() + stderr.read()
                _, stdout, stderr = ssh_client.exec_command(
                    DOJOSENSEI_COMMANDS.get("conf_ttyd_on_rport")
                )
                stdout = stdout.readlines() + stderr.readlines()
                result["imagebox"]["stdout"] = str(stdout)
                json_output = stdout[stdout.index(DOJOSENSEI_JSON_DATA_SEP) + 1]
                json_output = json.loads(json_output)
                result["imagebox"]["stdout"] = json_output
                result["imagebox"][
                    "accessUrl"
                ] = f"http://{json_output['data']['lhost']}:{json_output['data']['lport']}"
            except SSHException as exc:
                print("Error:command conf_ttyd_on_rport:", exc)
                raise HTTPException(status.HTTP_409_CONFLICT, str(exc)) from exc
    return result

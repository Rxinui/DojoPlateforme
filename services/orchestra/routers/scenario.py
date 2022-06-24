"""FastAPI router scenario

@author Rxinui
"""

from email import header
import os
from typing import Dict, Any
import httpx
from fastapi import APIRouter, status, Request, HTTPException

router = APIRouter(tags=["scenario"])
API_VBOX_URL: str = os.environ["API_VBOX_URL"]
API_VBOX_TIMEOUT_SEC: int = 300 # 5 min

@router.post("/scenario/start_workshop", status_code=status.HTTP_200_OK)
async def scenario_start_workshop(request: Request, params: Dict[str, Any]):
    """[Scenario] Start a workshop.

    "Workshop" is product term to specify "VM environment".

    Scenario:
        1. Create a new instance of .ova image
        2. Start the new instance created
        3. Request rportd the instance's out port
        4. Return the result data

    Input: Dict
        vmname: # required by /import and /startvm
        image: # required by /import
        type: # optional, by /startvm

    Output: #wip
        workshop:
            title:
            author:
        box:
            protocol: VNC | HTTP
            url_access:

    Returns:
        _type_: _description_
    """
    result = dict(box={},workshop={})
    headers = {"Authorization": request.headers.get("Authorization")}
    async with httpx.AsyncClient(base_url=API_VBOX_URL, headers=headers, timeout=API_VBOX_TIMEOUT_SEC) as api_vbox:
        ## 1. Create a new instance of .ova image
        response = await api_vbox.post("/import", json=params)
        if response.status_code != status.HTTP_202_ACCEPTED:
            raise HTTPException(status.HTTP_409_CONFLICT,response.json())
        ## 2. Start the new instance created
        response = await api_vbox.post("/startvm", json=params)
        if response.status_code != status.HTTP_202_ACCEPTED:
            raise HTTPException(status.HTTP_409_CONFLICT,response.json())
    return {"box": response.json()}

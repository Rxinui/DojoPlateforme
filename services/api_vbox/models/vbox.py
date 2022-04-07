"""Models for `api_vbox` used by FastAPI app.

@author Rxinui
@date 2022-04-04
@see https://fastapi.tiangolo.com/
"""
from pathlib import Path
from typing import List, Optional, Union
from pydantic import BaseModel


class OvfSessionParams(BaseModel):
    """Datamodel for OVF session parameters.

    Attributes:
        image (Path[str]): specify ovf image path
        vmname (str): name to assign to the vm
        options (List[bool]): options to keep in the following order
                              between 'keepallmacs', 'keepnatmacs', 'importtovdi'
        vsys (Union[int, str]): virtual system to use
        expires_in (Optional[int]): time to live in seconds of the vm. Specify when to delete it.
    """

    image: Path[str] = ...
    vmname: str = ...
    options: List[bool] = []
    vsys: Union[int, str] = 0
    expires_in: Optional[int] = 0

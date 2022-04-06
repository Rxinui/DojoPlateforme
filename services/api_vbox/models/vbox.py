"""Models for `api_vbox` used by FastAPI app.

@author Rxinui
@date 2022-04-04
@see https://fastapi.tiangolo.com/
"""
from pathlib import Path
from typing import List, Optional, Union
from pydantic import BaseModel

class OvfSessionParams(BaseModel):

    image: Path[str] = ...
    vmname : str = ...
    options : List[bool] = []
    vsys : Union[int,str] = 0


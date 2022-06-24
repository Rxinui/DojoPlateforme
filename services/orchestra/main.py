"""Orchestra controller service powered with Python and FastAPI.

@author Rxinui
"""
import json
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from routers import scenario as route_scenario
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI()
app.include_router(route_scenario.router)

@app.exception_handler(StarletteHTTPException)
async def __http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail
    )

@app.get("/")
def home() -> dict:
    return dict(hello="world")
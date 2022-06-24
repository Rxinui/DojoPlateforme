"""API vbox powered with Python and FastAPI.

@author Rxinui
@date 2022-01-21
@see https://www.virtualbox.org/manual/ch08.html
"""
import json
import os
from dotenv import load_dotenv

load_dotenv()

from models import BasicError
from fastapi import FastAPI, status, Depends
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.openapi.utils import get_openapi
from starlette.exceptions import HTTPException as StarletteHTTPException
from dependencies.user import auth_strategy
from routers import list as route_list
from routers import import_ as route_import
from routers import startvm as route_startvm
from openapi import api_vbox_openapi
from utils import logger

logger = logger(__name__, f"{__file__}.log")

AuthStrategy = auth_strategy(tag=os.getenv("API_VBOX_AUTH_STRATEGY",""))
app = FastAPI(dependencies=[Depends(AuthStrategy)])
app.include_router(route_list.router)
app.include_router(route_import.router)
app.include_router(route_startvm.router)


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


@app.exception_handler(StarletteHTTPException)
async def __http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content=BasicError(
            code="BAD_HTTP_VALIDATION",
            error="HTTP Error",
            details=str(exc.detail),
        ).__dict__,
    )


@app.exception_handler(RequestValidationError)
async def __validation_exception_handler(request, exc):
    """Validation exception handler"""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=BasicError(
            code="BAD_REQUEST_VALIDATION",
            error="Error during HTTP arguments validation",
            details=exc.errors(),
        ).__dict__,
    )


@app.on_event("shutdown")
def shutdown_event():
    """
    Save new openapi schema.
    """
    with open("./openapi/openapi.json", "w", encoding="utf-8") as fo:
        json.dump(app.openapi(), fo, indent=2)

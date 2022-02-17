import json
from typing import Any, Dict

def api_vbox_openapi(openapi_schema: Dict[str,Any]):
    with open("openapi/openapi_security.json", encoding="utf-8") as fp:
        security = json.load(fp)
        print(openapi_schema.get("security"))
        if not openapi_schema.get("security"):
            openapi_schema.setdefault("security",[]).extend(security["security"])
        if not openapi_schema["components"].get("securitySchemes"):
            openapi_schema["components"].setdefault("securitySchemes",{}).update(
                security["components"]["securitySchemes"]
            )
    return openapi_schema
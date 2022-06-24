from .auth import *
from .scope import ReadScope, CreateScope, ControlScope

def auth_strategy(tag: str) -> object:
    """Select an auth strategy by one of its tags.

    Args:
        tag (str): auth strategy tag

    Returns:
        object: auth strategy class
    """
    tag = tag.lower().replace("_","").replace(" ","")
    if tag in {"httpbearertokenauth","httpbearerjwt","httpbearer"}:
        return HTTPBearerTokenAuth
    return NoAuth
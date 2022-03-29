from enum import Enum


class Scope(Enum):

    ALL = "api_vbox:all"
    READ = "api_vbox:read"
    CREATE = "api_vbox:create"
    CONTROL = "api_vbox:control"

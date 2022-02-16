"""Abstract classes for VBoxManage wrapper."""
from abc import ABC

class VBoxManageCommand(ABC):

    """
    Command-line CLI used to control VBoxManage
    """
    CLI : str = "VBoxManage"

"""
Python wrapper for VBoxManage command-line tool.

@author rly
@date 21/01/2022
@see https://www.virtualbox.org/manual/ch08.html
"""

from ._list import VBoxManageList


class VBoxManageBuilder:
    """
    Python class to build shell VBoxManage commands programatically.
    """

    __list: VBoxManageList = VBoxManageList()

    @classmethod
    def list(cls) -> VBoxManageList:
        """Return the unique list instance.

        Returns:
            VBoxManageList: list subcommand
        """
        return cls.__list

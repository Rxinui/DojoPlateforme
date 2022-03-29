"""
Python wrapper for VBoxManage command-line tool.

@author Rxinui
@date 2022-01-21
@see https://www.virtualbox.org/manual/ch08.html
"""

from ._list import VBoxManageList


class VBoxManageBuilder:
    """
    Python class to build shell VBoxManage commands programatically.
    """

    list: VBoxManageList = VBoxManageList()

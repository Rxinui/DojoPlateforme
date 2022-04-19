"""
Python builder for VBoxManage 'list' subcommand-line tool.

@author Rxinui
@date 2022-01-21
@see https://www.virtualbox.org/manual/ch08.html#vboxmanage-list
"""
from typing import List
from .._vboxcommand import VBoxManageCommand
from ._parser import VBoxManageListParser
from ._directives import VBoxManageListDirective


class VBoxManageList(VBoxManageCommand):
    """Python wrapper for `VBoxManage list`."""

    parser = VBoxManageListParser

    ORIGIN: str = "list"

    """Specify available directives by a User.

    Only directives listed below will be recognized by the API.

    Returns:
        List[str]: availables and valid directives.
    """
    DIRECTIVES: List[str] = parser.DIRECTIVES

    @property
    def vms(self) -> VBoxManageListDirective:
        """Specify 'vms' directive to list subcommand.

        Returns:
            (str): list vms command-line.
        """
        return VBoxManageListDirective(self, "vms")

    @property
    def runningvms(self) -> VBoxManageListDirective:
        """Specify 'runningvms' directive to list subcommand.

        Returns:
            (str): list runningvms command-line.
        """
        return VBoxManageListDirective(self, "runningvms")

    @property
    def intnets(self) -> VBoxManageListDirective:
        """Specify 'intnets' directive to list subcommand.

        Returns:
            (str): list intnets command-line.
        """
        return VBoxManageListDirective(self, "intnets")

    @property
    def hostinfo(self) -> VBoxManageListDirective:
        """Specify 'hostinfo' directive to list subcommand.

        Returns:
            (str): list hostinfo command-line.
        """
        return VBoxManageListDirective(self, "hostinfo")

    @property
    def groups(self) -> VBoxManageListDirective:
        """Specify 'groups' directive to list subcommand.

        Returns:
            (str): list groups command-line.
        """
        return VBoxManageListDirective(self, "groups")

    @property
    def systemproperties(self) -> VBoxManageListDirective:
        """Specify 'systemproperties' directive to list subcommand.

        Returns:
            (str): list systemproperties command-line.
        """
        return VBoxManageListDirective(self, "systemproperties")

    @property
    def bridgedifs(self) -> VBoxManageListDirective:
        """Specify 'bridgedifs' directive to list subcommand.

        Returns:
            (str): list bridgedifs command-line.
        """
        return VBoxManageListDirective(self, "bridgedifs")

    @property
    def hostonlyifs(self) -> VBoxManageListDirective:
        """Specify 'hostonlyifs' directive to list subcommand.

        Returns:
            (str): list hostonlyifs command-line.
        """
        return VBoxManageListDirective(self, "hostonlyifs")

    @property
    def natnets(self) -> VBoxManageListDirective:
        """Specify 'natnets' directive to list subcommand.

        Returns:
            (str): list natnets command-line.
        """
        return VBoxManageListDirective(self, "natnets")

    @property
    def dhcpservers(self) -> VBoxManageListDirective:
        """Specify 'dhcpservers' directive to list subcommand.

        Returns:
            (str): list dhcpservers command-line.
        """
        return VBoxManageListDirective(self, "dhcpservers")

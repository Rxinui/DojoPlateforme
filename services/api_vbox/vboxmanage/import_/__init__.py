"""
Python builder for VBoxManage 'import' subcommand-line tool.

@author Rxinui
@date 2022-04-04
@see https://www.virtualbox.org/manual/ch08.html#vboxmanage-import
"""
from .._vboxcommand import VBoxManageCommand
from ._directives import VBoxManageImportDirective
from ._parser import VBoxManageImportParser

class VBoxManageImport(VBoxManageCommand):
    """Python wrapper for `VBoxManage import`."""

    parser = VBoxManageImportParser

    ORIGIN: str = "import"

    def __init__(self) -> None:
        super().__init__()
        self._cmd.append(self.ORIGIN)

    def ovf(self, ovfname: str) -> VBoxManageImportDirective:
        """Specify 'ovfname' directive to import subcommand.

        Returns:
            (str): import ovf command-line.
        """
        return VBoxManageImportDirective(self, ovfname)

    def ova(self, ovaname: str) -> VBoxManageImportDirective:
        """Specify 'ova' directive to import subcommand.

        It is an alias of ovf method.

        Returns:
            (str): import ovf command-line.
        """
        return self.ovf(ovaname)

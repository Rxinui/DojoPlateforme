"""
Python directive for VBoxManageImport builder.

@author Rxinui
@date 2022-04-04
@see https://www.virtualbox.org/manual/ch08.html#vboxmanage-import
"""
from typing import Dict, Optional, Union
from .._vboxcommand import VBoxManageDirective, VBoxManageCommand


class VBoxManageImportDirective(VBoxManageDirective):

    """General 'import' directive in-one class"""

    def __init__(
        self, vbox_command: VBoxManageCommand, directive: str, vsys: int = 0
    ) -> None:
        """Initialize {directive} of the given 'import' command.

        Args:
            vbox_command (VBoxManageCommand): VBoxManage command
            directive (str): directive used by VBoxManage command
        """
        super().__init__(vbox_command, directive)
        self._set_option("--vsys", str(vsys))

    def dry_run(self, flag: bool = True) -> "VBoxManageImportDirective":
        """Add 'dry-run' flag to commands.

        Args:
            flag (bool, optional): enable 'dry-run'. Defaults to True.

        Returns:
            VBoxManageImportDirective: updated directive
        """
        self._set_option("-n", flag)
        return self

    def options(
        self,
        keepallmacs: bool = False,
        keepnatmacs: bool = False,
        importtovdi: bool = False,
    ) -> "VBoxManageImportDirective":
        """Add 'options' flag to commands.

        Args:
            keepallmacs (bool, optional): enable 'keepallmacs'. Defaults to False.
            keepnatmacs (bool, optional): enable 'keepnatmacs'. Defaults to False.
            importtovdi (bool, optional): enable 'importtovdi'. Defaults to False.

        Returns:
            VBoxManageImportDirective: updated directive
        """
        flags = []
        if keepallmacs:
            flags.append("keepallmacs")
        if keepnatmacs:
            flags.append("keepnatmacs")
        if importtovdi:
            flags.append("importtovdi")
        if flags:
            self._set_option("--options", ",".join(flags))
        return self

    def vmname(self, name: str) -> "VBoxManageImportDirective":
        """Add 'vmname' flag to commands.

        Args:
            name (str): updated directive
        """
        self._set_option("--vmname", name)
        return self

    def cloud(self, flag: bool = True) -> "VBoxManageImportDirective":
        """Add 'cloud' flag to commands.

        Args:
            flag (bool, optional): enable 'cloud'. Defaults to True.

        Returns:
            VBoxManageImportDirective: updated directive
        """
        self._set_option("--cloud", flag)
        return self

    def vsys(
        self, vsys: int, **kwargs: Optional[Dict[str, Union[bool, str, int]]]
    ) -> "VBoxManageImportDirective":
        """Add options display by the flag --dry-run.

        Those options depend on the ovf imported. Therefore,
        **kwargs must be in accordance with the ovf's options.

        Args:
            vsys (int): virtual system number

        Returns:
            VBoxManageImportDirective: updated directive
        """
        self._options["--vsys"] = str(vsys)
        for flag, value in kwargs.items():
            if not isinstance(value, bool):
                value = str(value)
            self._set_option(f"--{flag}", value)
        return self

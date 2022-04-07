"""
Python parser for VBoxManage 'list' builder.

@author Rxinui
@date 2022-01-21
@see https://www.virtualbox.org/manual/ch08.html#vboxmanage-list
"""
import re
from typing import Dict, Tuple


class VBoxManageListParser:
    """
    Parser for VBoxManageList command result.
    """

    DIRECTIVES = [
        "vms",
        "runningvms",
        "intnets",
        "hostinfo",
        "groups",
        "systemproperties",
        "bridgedifs",
        "hostonlyifs",
        "natnets",
        "dhcpservers",
    ]

    @staticmethod
    def __parse_key_value(k: str, v: str) -> Tuple[str, str]:
        k = k.strip().lower().replace(" ", "_")  # replace whitespace as underscore
        k = re.sub(r"[)(,\.]", "", k)  # remove special chars
        return k, v.strip()

    @staticmethod
    def parse_vms(output: str, long: bool = False) -> Dict[str, str]:
        """
        Retrieve vbox name and vbox uuid from `VBoxManage list vms`.

        Args:
            output (str): output from command

        Returns:
            (Dict[str,str]): vbox id as key and vbox name as value of the dict
        """

        def parse_short_vms() -> Dict[str, str]:
            """
            Example:
                before: '"pmint_box_dev-1" {77bd1e0e-edc6-47fc-807a-987c296c64dd}'
                after: {"pmint_box_dev-1": "77bd1e0e-edc6-47fc-807a-987c296c64dd"}
            """
            get_vm = lambda l: re.search(r"\"([\._\d\w-]+)\"\s+\{([\d\w-]+)\}", l.strip())
            vms = {}
            for line in output.splitlines():
                if line:
                    vm = get_vm(line)
                    vms[vm.group(2)] = vm.group(1)
            return vms

        def parse_long_vms() -> Dict[str, str]:
            sep_vm = "\n\n\n"
            vms = {}
            for vm_info in output.split(sep_vm):
                vm = {}
                if vm_info:
                    for info in vm_info.splitlines():
                        match = re.search(r"^([\d\w\s)(,-/]+):(.*)", info)
                        if match:
                            (
                                info_desc,
                                info_value,
                            ) = VBoxManageListParser.__parse_key_value(
                                match.group(1), match.group(2)
                            )
                            if (
                                info_value == "<none>"
                                or info_value == ""
                                or not info_value
                            ):
                                info_value = None
                            vm[info_desc] = info_value
                    vms[vm["uuid"]] = vm
            return vms

        return parse_long_vms() if long else parse_short_vms()

    @staticmethod
    def parse_runningvms(output: str, long: bool = False) -> Dict[str, str]:
        """
        Retrieve vbox name and vbox uuid from `VBoxManage list runningvms`.

        Example:
            before: '"pmint_box_dev-1" {77bd1e0e-edc6-47fc-807a-987c296c64dd}'
            after: {"pmint_box_dev-1": "77bd1e0e-edc6-47fc-807a-987c296c64dd"}

        Args:
            output (str): output from command

        Returns:
            (Dict[str,str]): vbox id as key and vbox name as value of the dict
        """
        return VBoxManageListParser.parse_vms(output, long)

    @staticmethod
    def parse_hostinfo(output: str, long: bool = False) -> Dict[str, str]:
        """
        Retrieve host info with vbox uuid or name from `VBoxManage list hostinfo`.

        Args:
            output (str): output from command
            long (bool): long hostinfo is the same as hostinfo

        Returns:
            (Dict[str,str]): vbox host info description as key and host info value as value
        """
        parsed = {}
        for line in output.splitlines()[2:]:
            info_desc, info_value = VBoxManageListParser.__parse_key_value(
                *line.split(": ")
            )
            parsed[info_desc] = info_value
        return parsed

    @staticmethod
    def get_directives_regex() -> str:
        """Returns VBoxManageList availables directives in a regex form.

        Returns:
            List[str]: regex of all directives
        """
        return f"^(({'|'.join(VBoxManageListParser.DIRECTIVES)}),?)+$"

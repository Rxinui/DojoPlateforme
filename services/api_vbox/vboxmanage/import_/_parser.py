"""
Python parser for VBoxManage 'import' builder.

@author Rxinui
@date 2022-04-04
@see https://www.virtualbox.org/manual/ch08.html#vboxmanage-import
"""

from typing import Dict


class VBoxManageImportParser:
    """
    Parser for VBoxManageList command result.
    """

    @staticmethod
    def parse_result(out: str, exit_code: int) -> Dict[str, str]:
        """Parse `VBoxManage import` command result.

        Args:
            out (str): stderr from result
            exit_code (int): exit code from result

        Returns:
            Dict[str, str]: parsed result
        """
        if exit_code != 0:
            ind = out.find("Progress state:")
            if ind >= 0 :
                return {"result": out[ind:]}
        return {"result": out.split("\n")[-2]}

import typing
from common.CLI.module import CLImodule

class UserInterfaceHandler:
    interfaces: typing.Dict[str, CLImodule] = {}
    
    def __init__(self, interfaces: typing.List[CLImodule]):
        self.interfaces = {interface.module_name: interface for interface in interfaces}
        
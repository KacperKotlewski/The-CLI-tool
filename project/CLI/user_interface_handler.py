import typing
from common.CLI.model import CLI_Model

class UserInterfaceHandler:
    interfaces: typing.Dict[str, CLI_Model] = {}
    
    def __init__(self, interfaces: typing.List[CLI_Model]):
        self.interfaces = {interface.module_name: interface for interface in interfaces}
        
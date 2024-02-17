from .module import Module

import typing

class RootModule(Module):
    user_interfaces: typing.List["UserInterface"] = list()
    
    def __init__(self, **data) -> None:
        super().__init__(**data)
        
    def _validate(self) -> None:
        """
        _validate validates the root module.
        """
        self._validate_user_interfaces()
        return super()._validate()
    
    def _validate_user_interfaces(self) -> None:
        """
        _validate_user_interfaces validates the user interfaces of the root module.
        """
        list_of_names = [user_interface.name for user_interface in self.user_interfaces]
        if len(list_of_names) != len(set(list_of_names)):
            raise ValueError(f"RootModule {self.name} has duplicate user interface names: \n{list_of_names}")
        
        for user_interface in self.user_interfaces:
            user_interface._validate()
            
    def add_user_interface(self, user_interface: "UserInterface") -> None:
        """
        add_user_interface adds a user interface to the root module.
        
        Args:
            user_interface (UserInterface): The user interface to add to the root module.
        """
        if user_interface not in self.user_interfaces:
            self.user_interfaces.append(user_interface)
            self._validate_user_interfaces()
            
    def remove_user_interface(self, user_interface: "UserInterface") -> None:
        """
        remove_user_interface removes a user interface from the root module.
        
        Args:
            user_interface (UserInterface): The user interface to remove from the root module.
        """
        if user_interface in self.user_interfaces:
            self.user_interfaces.remove(user_interface)
            self._validate_user_interfaces()
            
    def get_user_interface(self, name: str) -> "UserInterface":
        """
        get_user_interface gets a user interface from the root module by name.
        
        Args:
            name (str): The name of the user interface to get from the root module.
        """
        for user_interface in self.user_interfaces:
            if user_interface.name == name:
                return user_interface
        raise ValueError(f"RootModule {self.name} has no user interface with name {name}")
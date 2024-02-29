from .interface_class import Interface


class UserInterface(Interface):
    """
    UserInterface class is the user interface class.
    
    """
    name: str = ""
    description: str = ""
    
    def __init__(self, **data) -> None:
        return super().__init__(**data)
    
    
from abc import ABC, abstractmethod
import typing

from .abstract_model import AbstractModel

class AbstractHandler(ABC):
    """
    AbstractHandler class is a class that represents a handler.
    
    Args:
        items (List[AbstractModel]): The items of the handler.
    """
    items_instance: typing.Type
    items: typing.List[AbstractModel]
    
    @abstractmethod
    def _validate(self) -> None:
        """
        _validate validates the items of the handler.
        """
        self._validate_items()
        
    @abstractmethod
    def _validate_items(self) -> None:
        """
        _validate_items validates the items of the handler.
        """
        self._validate_duplicates()
        
        for item in self.items:
            item._validate()
        
    @abstractmethod
    def _validate_duplicates(self) -> None:
        """
        _validate_duplicates validates the items of the handler for duplicates.
        """
        list_of_names = [item.name for item in self.items]
        if len(list_of_names) != len(set(list_of_names)):
            raise ValueError(f"Handler has duplicate names: \n{list_of_names}")
        
    @abstractmethod
    def verify_item(self, item: AbstractModel) -> bool:
        """
        verify_item verifies the item to be added to the handler.
        
        Args:
            item (Any): The item to verify.
        """
        self.check_item_instance(item)
        item._validate()
        self.check_item_duplicates(item)
        return True
        
    @abstractmethod
    def check_item_duplicates(self, item: typing.Any) -> bool:
        """
        check_item_duplicates checks the item for duplicates.
        
        Args:
            item (Any): The item to check for duplicates.
        """
        if item in self.items:
            raise ValueError(f"Item {item} already exists in the handler.")
        return True
        
    @abstractmethod
    def check_item_instance(self, item: typing.Any) -> bool:
        """
        check_item_instance checks the item to be an instance of AbstractModel.
        
        Args:
            item (Any): The item to check to be an instance of AbstractModel.
        """
        if not isinstance(item, AbstractModel):
            raise ValueError(f"Item {item} is not an instance of AbstractModel.")
        if not (isinstance(item, self.items_instance) or issubclass(item, self.items_instance)):
            raise ValueError(f"Item {item} is not an instance of {self.items_instance}.")
        return True
    
    @abstractmethod 
    def add(self, item: typing.Any) -> None:
        """
        add adds an item to the handler.
        
        Args:
            item (Any): The item to add to the handler.
        """
        self.verify_item(item)
        if item not in self.items:
            self.items.append(item)
            self._validate_items()
            
    @abstractmethod
    def extend(self, items: typing.List[typing.Any]) -> None:
        """
        extend extends the handler with a list of items.
        
        Args:
            items (List[Any]): The items to extend the handler with.
        """
        for item in items:
            self.add(item)
            
    @abstractmethod
    def insert(self, index: int, item: typing.Any) -> None:
        """
        insert inserts an item into the handler at the given index.
        
        Args:
            index (int): The index to insert the item into the handler.
            item (Any): The item to insert into the handler.
        """
        if item not in self.items:
            self.items.insert(index, item)
            self._validate_items()

    @abstractmethod
    def remove(self, item: typing.Any) -> None:
        """
        remove removes an item from the handler.
        
        Args:
            item (Any): The item to remove from the handler.
        """
        if item in self.items:
            self.items.remove(item)
            self._validate_items()
            
    @abstractmethod
    def get(self, name: str) -> typing.Any:
        """
        get gets an item from the handler by name.
        
        Args:
            name (str): The name of the item to get from the handler.
            
        Returns:
            Any: The item from the handler by name.
        """
        for item in self.items:
            if item.name == name:
                return item
        raise ValueError(f"Item {name} does not exist in the handler.")
    
    @abstractmethod    
    def execute(self, name: str, *args) -> typing.Any:
        """
        execute executes an item from the handler by name.
        
        Args:
            name (str): The name of the item to execute from the handler.
            *args: The arguments to pass to the item
        """
        item = self.get(name)
        return item(*args)
    
    @abstractmethod
    def __len__(self) -> int:
        """
        __len__ gets the length of the handler.
        
        Returns:
            int: The length of the handler.
        """
        return len(self.items)
    
    @abstractmethod
    def __iter__(self) -> typing.Iterator:
        """
        __iter__ iterates the handler.
        
        Returns:
            Iterator: The iterator of the handler.
        """
        return iter(self.items)
    
    @abstractmethod
    def __lt__(self, other: 'AbstractHandler') -> bool:
        """
        __lt__ checks if the handler is less than another handler.
        
        Args:
            other (AbstractHandler): The other handler to compare to.
            
        Returns:
            bool: True if the handler is less than the other handler, False otherwise.
        """
        return len(self) > len(other)
    
    @abstractmethod
    def __add__(self, other: typing.Union['AbstractHandler', typing.Any, typing.List[typing.Any]]) -> 'AbstractHandler':
        """
        __add__ adds an item or list of items to the handler.
        
        Args:
            other (Union[Any, List[Any]]): The item or list of items to add to the handler.
            
        Returns:
            AbstractHandler: The handler with the item or list of items added.
        """
        if isinstance(other, list):
            self.extend(other)
                
        elif isinstance(other, self.__class__):
            self.__add__(other.items)
            
        elif self.check_item_instance(other):
            self.add(other)
            
        else:
            raise ValueError(f"Cannot add {other.__class__} to {self.__class__}")
        
        return self
    
    def stylized_representation(self, total_space:int=None, space_before:int=None, space_after:int=None, first_str_lenght:int=None, second_str_lenght:int=None) -> str:
        """
        stylized_presentation stylizes the presentation of the handler.
        
        Args:
            total_space (int): The total space. Default is None.
            space_before (int): The space before the handler. Default is None.
            space_after (int): The space after the handler. Default is None.
            first_str_lenght (int): The length of the first string. Default is None.
            second_str_lenght (int): The length of the second string. Default is None.
        """
        
        return [item.stylized_representation(total_space, space_before, space_after, first_str_lenght, second_str_lenght) for item in self.items]    
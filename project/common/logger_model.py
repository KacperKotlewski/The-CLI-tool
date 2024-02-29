from abc import ABC, abstractmethod
from common.models.base import BaseModel
from common.debug import DEBUG

class LoggerModel(ABC, BaseModel):
    """
    LoggerModel is an abstract class that provides a log method to all classes that inherit from it.
    """
    
    @classmethod
    def get_log_position(cls, *args, **kwargs):
        return f"{cls.__name__}: "
    
    @classmethod
    def log_strict(cls, *args, **kwargs):
        DEBUG.log_matching_keyword(cls.__name__, cls.get_log_position(), *args, **kwargs)
    
    @classmethod
    def log_error(cls, *args, **kwargs):
        DEBUG.elog(cls.get_log_position(), *args, **kwargs)
        
    @classmethod
    def log_on_debug(cls, *args, **kwargs):
        DEBUG.dlog(cls.get_log_position(), *args, **kwargs)
import typing
from common.models.base import BaseModel, ValidationError
import warnings
import pytest

class TestBaseModel(BaseModel):
    __test__ = False
    value1: str = None
    value2: bool = None
    value3: typing.List[str] = list()
    value4: typing.Dict[str, str] = dict()
    value5: typing.Optional[str] = None
    
def test_base_model_copy():
    """
    test_base_model test BaseModel
    """
    model = TestBaseModel()
    model.value1 = "value1"
    model.value2 = True
    model.value3 = ["value3"]
    model.value4 = {"key": "value"}
    
    copy = model.Copy()
    
    assert copy.value1 == model.value1 == "value1"
    assert copy.value2 == model.value2 == True
    assert copy.value3 == model.value3 == ["value3"]
    assert copy.value4 == model.value4 == {"key": "value"}
    assert copy.value5 == model.value5 == None
    
def test_base_model_copy_invalid():
    """
    test_base_model test BaseModel
    """
    model = TestBaseModel()
    
    try:
        model.Copy()
    except Exception as e:
        assert isinstance(e, ValidationError)
    else:
        assert False, "TypeError exception not raised"
    
def test_base_model_copy_filtered():
    """
    test_base_model_filtered test BaseModel
    """
    model = TestBaseModel()
    model.value2 = True
    
    copy = model.CopyFiltered()
    
    assert copy.value1 == model.value1 == None
    assert copy.value2 == model.value2 == True
    assert copy.value3 == model.value3 == []
    assert copy.value4 == model.value4 == {}
    assert copy.value5 == model.value5 == None
    
@pytest.mark.filterwarnings("ignore::UserWarning")
def test_base_model_copy_filtered_invalid():
    """
    test_base_model_filtered test BaseModel
    """
    model = TestBaseModel()
    
    model.value1 = True
        
    try:
        model.CopyFiltered()
    except Exception as e:
        assert isinstance(e, ValidationError)
    else:
        assert False, "ValidationError exception not raised"
    
def test_base_model_is_valid():
    """
    test_base_model_is_valid test BaseModel
    """
    model = TestBaseModel()
    model.value1 = "value1"
    model.value2 = True
    model.value3 = ["value3"]
    model.value4 = {"key": "value"}
    
    assert model.isValid() == True


@pytest.mark.filterwarnings("ignore::UserWarning")
def test_base_model_is_valid_invalid():
    """
    test_base_model_is_valid test BaseModel
    """
    model = TestBaseModel()
        
    assert model.isValid() == False
    
def test_base_model_is_valid_filtered():
    """
    test_base_model_is_valid_filtered test BaseModel
    """
    model = TestBaseModel()
    model.value2 = True
    
    assert model.isValidFiltered() == True
    
@pytest.mark.filterwarnings("ignore::UserWarning")
def test_base_model_is_valid_filtered_invalid():
    """
    test_base_model_is_valid_filtered test BaseModel
    """
    model = TestBaseModel()
    
    model.value1 = True
        
    assert model.isValidFiltered() == False
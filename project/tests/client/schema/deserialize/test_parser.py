import pytest
from client.schema.deserialize import parser

def test_get_key_and_value():
    lines = {
        "some_key : some_value": ("some_key", "some_value"),
        "key_int : 123": ("key_int", "123"),
        "key_list1 : x,y,z": ("key_list1", "x,y,z"),
        "key_list2 : [x,y,z]": ("key_list2", "[x,y,z]"),
    }
    
    for line, expected in lines.items():
        (key,value) = parser.get_key_and_value(line)
        assert key == expected[0]        
        assert value == expected[1]        
    
    
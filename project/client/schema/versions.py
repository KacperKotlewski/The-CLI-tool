import re

VALID_SCHEMA_VERSIONS = [
    "0.1", "0.1.1",
]

def checkVersion(version:str) -> bool:
    if version in VALID_SCHEMA_VERSIONS:
        return True
    if 'x' in version.lower():
        vsplit = version.split(".")
        for validV in VALID_SCHEMA_VERSIONS:
            validVsplit = validV.split(".")
            if vsplit[0] == validVsplit[0]:
                for i,v in enumerate(vsplit[1:]):
                    if v.lower() == "x":
                        return True
                    elif v.lower() != validVsplit[i+1].lower():
                        break
    return False
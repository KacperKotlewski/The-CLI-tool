import pytest
from client.schema.versions import checkVersion, VALID_SCHEMA_VERSIONS

def test_checkVersion():
    validVersions = VALID_SCHEMA_VERSIONS + ["0.x", "0.x.x", "0.1.x"]
    notValidVersions = ["x.x", "invalid", "9999.9999"]
    
    for version in validVersions:
        assert checkVersion(version), f"Version '{version}' should be valid"

    for version in notValidVersions:
        assert not checkVersion(version), f"Version '{version}' should be invalid"
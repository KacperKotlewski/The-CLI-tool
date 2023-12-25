import pytest
from client.schema.versions import Version, InvalidVersion
    
def test_latest():
    latest = Version.getLatest()
    latestMajor = Version.getLatestMajor()
    
    assert latest == Version.v0_1_1
    assert latestMajor == "0" 

def test_check():
    validVersions = Version.getAllStr() + ["0.x", "0.x.x", "0.1.x"]
    notValidVersions = ["x.x", "invalid", "9999.9999"]
    
    for version in validVersions:
        assert Version.check(version), f"Version '{version}' should be valid"

    for version in notValidVersions:
        assert not Version.check(version), f"Version '{version}' should be invalid"
        
def test_version_content():
    versions = Version.getAll()
    versionsStr = Version.getAllStr()
    
    assert len(versions) == len(versionsStr)
    assert versions != versionsStr
    assert len(versions) == len(Version)
    
def test_match():
    version = Version.v0_1_1.value
    assert Version.match(version) == Version.v0_1_1
    
def test_match_invalid():
    version = "invalid"
    with pytest.raises(InvalidVersion):
        Version.match(version)

def test_fetch():
    versions = Version.getAllStr() + ["0.x", "0.x.x", "0.1.x"]
    
    for version in versions:
        if "x" in version:
            assert Version.fetch(version) == Version.getLatest()
        else:
            assert Version.fetch(version).value == version
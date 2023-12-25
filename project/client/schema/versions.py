import enum
import typing

class InvalidVersion(Exception):
    pass

class Version(enum.Enum):
    v0_1 = "0.1"
    v0_1_1 = "0.1.1"

    @staticmethod
    def getAll() -> typing.List['Version']:
        return [v for v in Version]

    @staticmethod
    def getAllStr() -> typing.List[str]:
        return [v.value for v in Version]

    @staticmethod
    def getLatest() -> 'Version':
        return Version.getAll()[-1]

    @staticmethod
    def getLatestMajor() -> str:
        return Version.getAll()[-1].value.split(".")[0]

    @staticmethod
    def check(version: str) -> bool:
        if version in Version.getAllStr():
            return True
        if 'x' in version.lower():
            vsplit = version.split(".")
            for validV in Version.getAllStr():
                validVsplit = validV.split(".")
                if vsplit[0] == validVsplit[0]:
                    for i, v in enumerate(vsplit[1:]):
                        if v.lower() == "x":
                            return True
                        elif i + 1 < len(validVsplit) and v.lower() != validVsplit[i + 1].lower():
                            break
        return False

    @staticmethod
    def match(version_str: str) -> 'Version':
        for v in Version:
            if v.value == version_str:
                return v
        raise InvalidVersion(f"Version string '{version_str}' does not match any Version enum")

    @staticmethod
    def fetch(version: str) -> 'Version':
        if version in Version.getAllStr():
            return Version.match(version)
        if 'x' in version.lower():
            vsplit = version.split(".")
            reversed_versions = Version.getAllStr()
            reversed_versions.reverse()
            for validV in reversed_versions:
                validVsplit = validV.split(".")
                if vsplit[0] == validVsplit[0]:
                    for i, v in enumerate(vsplit[1:]):
                        if v.lower() == "x" or (i + 1 < len(validVsplit) and v.lower() == validVsplit[i + 1].lower()):
                            return Version.match(validV)
                        elif i + 1 >= len(validVsplit) or v.lower() != validVsplit[i + 1].lower():
                            break
        raise InvalidVersion(f"Invalid version: {version}")

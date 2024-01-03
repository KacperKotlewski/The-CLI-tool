from pydantic import ValidationError, BaseModel as PydanticBaseModel


class BaseModel(PydanticBaseModel):
    def Copy(self):
        """
        Copy all values to a new model
        """
        data = self.model_dump()
        new_model = self.__class__(**data)
        return new_model

    def CopyFiltered(self):
        """
        Copy filtered values to a new model
        Filtered values:
            - None
        """
        data = {k: v for k, v in self.model_dump(exclude_none=True,exclude_defaults=True).items() if v is not None}
        new_model = self.__class__(**data)
        return new_model

    def isValid(self) -> bool:
        """
        Validate model
        """
        try:
            copy = self.Copy()
            del copy
        except ValidationError:
            return False
        else:
            return True
        
    def isValidFiltered(self) -> bool:
        """
        Validate model
        """
        try:
            copy = self.CopyFiltered()
            del copy
        except ValidationError:
            return False
        else:
            return True
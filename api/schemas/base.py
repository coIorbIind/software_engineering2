from pydantic import BaseConfig, BaseModel


class BaseSchema(BaseModel):

    class Config(BaseConfig):
        orm_mode = True

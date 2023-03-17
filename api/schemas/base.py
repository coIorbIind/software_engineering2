from pydantic import BaseConfig, BaseModel


class BaseSchema(BaseModel):

    class Config(BaseConfig):
        orm_mode = True


class LimitOffsetPaginationSchema(BaseSchema):
    limit: int
    offset: int
    total: int


class PaginatedResponse(BaseSchema):
    data: list
    pagination: LimitOffsetPaginationSchema

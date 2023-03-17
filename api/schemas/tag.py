from api.schemas.base import BaseSchema


class TagBaseSchema(BaseSchema):
    id: int
    name: str
    code: str

from datetime import datetime
import typing

from api.schemas.base import BaseSchema
from api.schemas.tag import TagBaseSchema


class ArticleBaseSchema(BaseSchema):
    name: str
    code: str
    content: str
    author: str


class ArticleCreateSchema(ArticleBaseSchema):
    tags: typing.Optional[typing.List[str]]


class ArticleListSchema(ArticleBaseSchema):
    created_at: datetime
    tags: typing.List[TagBaseSchema]

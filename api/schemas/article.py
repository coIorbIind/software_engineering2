from datetime import datetime
import typing
from pydantic import BaseModel

from api.schemas.base import BaseSchema
from api.schemas.tag import TagBaseSchema


class ArticleBaseSchema(BaseSchema):
    name: str
    code: str
    content: str
    author: str


class ArticlePatchSchema(BaseSchema):
    name: typing.Optional[str]
    code: typing.Optional[str]
    content: typing.Optional[str]
    author: typing.Optional[str]
    tags: typing.Optional[list[str]]


class ArticlePutSchema(BaseSchema):
    name: str
    code: str
    content: str
    author: str
    tags: list[str]


class ArticleCreateSchema(ArticleBaseSchema):
    tags: typing.Optional[list[str]]


class ArticleListSchema(ArticleBaseSchema):
    created_at: datetime
    tags: list[TagBaseSchema]


class ArticleFilterSchema(BaseModel):
    name: typing.Optional[str] = None
    code: typing.Optional[str] = None
    content: typing.Optional[str] = None
    author: typing.Optional[str] = None


class PaginationInSearchSchema(BaseModel):
    limit: int = 5
    offset: int = 0


class ArticleSearchSchema(BaseModel):
    filter: ArticleFilterSchema
    pagination: PaginationInSearchSchema

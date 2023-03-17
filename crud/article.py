from typing import Optional
from datetime import datetime

from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import Field
from sqlalchemy import insert
from sqlalchemy.orm import Session, joinedload, Query

from db import Article, Tag, ArticleTag
from logic.execptions import ObjectNotFound
from api.schemas.article import ArticleCreateSchema


class ArticleFilter(Filter):
    """ Фильтр для статей """
    name__in: Optional[list[str]] = Field(alias='names')
    code__in: Optional[list[str]] = Field(alias='codes')

    class Constants(Filter.Constants):
        model = Article

    class Config:
        allow_population_by_field_name = True


def get_articles(session: Session, filter_obj: ArticleFilter, joined_load: Optional[tuple] = None) -> Query:
    """ Список статей """
    return filter_obj.filter(session.query(Article).options(joinedload(joined_load)))


def get_article_by_code(
    session: Session,
    code: str,
    joined_load: Optional[tuple] = None
) -> Optional[Article]:
    """ Получение объекта статьи """
    query = session.query(Article).filter(Article.code == code)
    if joined_load:
        query = query.options(*[joinedload(table) for table in joined_load])
    return query.first()


def get_article_by_code_or_404(
    session: Session,
    code: str,
    joined_load: Optional[tuple] = None
) -> Article:
    """ Получение статьи. 404 ошибка, если она не найдена """
    obj = get_article_by_code(session, code, joined_load)
    if not obj:
        raise ObjectNotFound
    return obj


def create_article(
    session: Session,
    article: ArticleCreateSchema
) -> Article:
    """ Создание статьи """
    data = article.dict()
    tags = data.pop('tags', None)
    obj = Article(**data, created_at=datetime.now())
    session.add(obj)
    session.commit()
    session.refresh(obj)

    if tags:
        tags_objs = session.query(Tag).filter(Tag.code.in_(tags))
        if tags_objs:
            values_to_add = [{'tag_id': tag.id, 'article_id': obj.id} for tag in tags_objs]
            session.execute(insert(ArticleTag).values(values_to_add))

    return obj

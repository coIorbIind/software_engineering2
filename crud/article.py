from typing import Optional
from datetime import datetime

from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import Field
from sqlalchemy import insert
from sqlalchemy.orm import Session, joinedload, Query

from db import Article, Tag, ArticleTag
from logic.execptions import ObjectNotFound
from api.schemas.article import ArticleCreateSchema, ArticlePutSchema, ArticlePatchSchema


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


def patch_article(
    session: Session,
    obj: Article,
    schema: ArticlePatchSchema | ArticlePutSchema
):
    dict_obj = schema.dict(exclude_unset=True)
    old_tags = {tag.code for tag in obj.tags}
    new_tags = dict_obj.pop('tags', None)
    for key, value in dict_obj.items():
        if hasattr(obj, key):
            setattr(obj, key, value)
    session.add(obj)
    session.commit()
    if new_tags is not None:
        update_article_tag(session, obj.id, old_tags, set(new_tags))

    session.refresh(obj)

    return obj


def update_article_tag(
    session: Session,
    article_id: int,
    old_tags: set[str],
    new_tags: set[str]
):
    to_delete = old_tags - new_tags
    to_create = new_tags - old_tags

    if to_delete:
        tags_ids = {tag.id for tag in session.query(Tag).filter(Tag.code.in_(to_delete))}
        if tags_ids:
            (
                session.query(ArticleTag)
                .filter(
                    ArticleTag.article_id == article_id,
                    ArticleTag.tag_id.in_(tags_ids)
                ).delete()
            )

    if to_create:
        tags_objs = session.query(Tag).filter(Tag.code.in_(to_create))
        if tags_objs:
            values_to_create = [{'tag_id': tag.id, 'article_id': article_id} for tag in tags_objs]
            session.execute(insert(ArticleTag).values(values_to_create))

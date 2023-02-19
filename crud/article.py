from typing import Optional
from datetime import datetime

from sqlalchemy import insert
from sqlalchemy.orm import Session, joinedload

from db import Article, Tag, ArticleTag
from execptions import ObjectNotFound
from api.schemas.article import ArticleCreateSchema


def get_article_by_code(
    session: Session,
    code: str,
    joined_load: Optional[tuple] = None
):
    query = session.query(Article).filter(Article.code == code)
    if joined_load:
        query = query.options(*[joinedload(table) for table in joined_load])
    return query.first()


def get_article_by_code_or_404(
    session: Session,
    code: str,
    joined_load: Optional[tuple] = None
):
    obj = get_article_by_code(session, code, joined_load)
    if not obj:
        raise ObjectNotFound
    return obj


def create_article(
    session: Session,
    article: ArticleCreateSchema
):
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

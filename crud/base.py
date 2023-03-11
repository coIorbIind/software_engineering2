from random import randint, choices
from typing import Optional

from sqlalchemy.orm import Session, joinedload
from faker import Faker

from db.base import Base, get_session
from db import Article, Tag, ArticleTag
from logic.execptions import ObjectNotFound


def get_object_or_404(
    session: Session,
    model: Base,
    pk: int,
    joined_load: Optional[tuple] = None
):
    query = session.query(model).filter(model.id == pk)
    if joined_load:
        query = query.options(*[joinedload(table) for table in joined_load])
    obj = query.first()
    if not obj:
        raise ObjectNotFound
    return obj


def seed_db():
    session = next(get_session())
    Base.metadata.create_all(bind=session.bind)
    faker = Faker()
    fake_article_slugs, fake_tag_slugs, fake_article_names, fake_tag_names = set(), set(), set(), set()
    for _ in range(100):
        fake_article_slugs.add(faker.slug())
        fake_tag_slugs.add(faker.slug())
        fake_article_names.add(faker.sentence())
        fake_tag_names.add(faker.word())
    fake_article_slugs = list(fake_article_slugs)
    fake_tag_slugs = list(fake_tag_slugs)
    fake_article_names = list(fake_article_names)
    fake_tag_names = list(fake_tag_names)
    length = min(len(fake_article_slugs), len(fake_article_names), len(fake_tag_slugs), len(fake_tag_names))
    articles = [
        Article(
            name=fake_article_names[i],
            code=fake_article_slugs[i],
            content=faker.text(),
            created_at=faker.date_time_this_decade(),
            author=faker.name()
        )
        for i in range(length)
    ]
    tags = [
        Tag(
            name=fake_tag_names[i],
            code=fake_tag_slugs[i],
        )
        for i in range(length)
    ]
    relations = []
    for article in articles:
        tags_count = randint(0, 4)
        tags_for_article = choices(tags, k=tags_count)
        for tag in tags_for_article:
            relations.append(ArticleTag(article=article, tag=tag))
    session.add_all(articles)
    session.add_all(tags)
    session.add_all(relations)
    session.commit()

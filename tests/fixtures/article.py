import pytest
import factory

from db import Article, ArticleTag


@pytest.fixture
def article_factory(scope_session, faker):
    faker.seed_instance(faker.random.randint(1, 10**6))

    class ArticleFactory(factory.alchemy.SQLAlchemyModelFactory):
        class Meta:
            model = Article
            sqlalchemy_session = scope_session
            sqlalchemy_session_persistence = 'commit'

        id = factory.Sequence(lambda i: 2000 + i)
        name = factory.Sequence(lambda i: faker.sentence() + str(i))
        code = factory.Sequence(lambda i: faker.slug() + str(i))
        content = faker.text()
        created_at = faker.date_time_this_decade()
        author = faker.name()

    return ArticleFactory


@pytest.fixture
def article_tag_factory(scope_session, article_factory, tag_factory):
    class ArticleTagFactory(factory.alchemy.SQLAlchemyModelFactory):
        class Meta:
            model = ArticleTag
            sqlalchemy_session = scope_session
            sqlalchemy_session_persistence = 'commit'

        article = factory.SubFactory(article_factory)
        tag = factory.SubFactory(tag_factory)

    return ArticleTagFactory

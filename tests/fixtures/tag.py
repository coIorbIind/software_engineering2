import pytest
import factory

from db import Tag


@pytest.fixture
def tag_factory(scope_session, faker):
    faker.seed_instance(faker.random.randint(1, 10**6))

    class ArticleFactory(factory.alchemy.SQLAlchemyModelFactory):
        class Meta:
            model = Tag
            sqlalchemy_session = scope_session
            sqlalchemy_session_persistence = 'commit'

        id = factory.Sequence(lambda i: 3000 + i)
        name = factory.Sequence(lambda i: faker.sentence() + str(i))
        code = factory.Sequence(lambda i: faker.slug() + str(i))

    return ArticleFactory

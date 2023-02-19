from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from sqlalchemy import or_

from db import Article
from api.routes.base import BaseRoute
from api.schemas.article import ArticleListSchema, ArticleCreateSchema
from crud.article import get_article_by_code_or_404, create_article
from execptions import UniqueFailed


router = InferringRouter()


@cbv(router)
class ArticleRoute(BaseRoute):
    model = Article

    @router.get('/{code}')
    def get_article(self, code: str) -> ArticleListSchema:
        return get_article_by_code_or_404(session=self.session, code=code, joined_load=('tags', ))

    @router.post('/')
    def create(self, article: ArticleCreateSchema) -> ArticleListSchema:
        self._validate_name_and_code(code=article.code, name=article.name)
        return create_article(self.session, article)

    def _validate_name_and_code(self, code: str, name: str):
        same_articles_count = self.session.query(Article).filter(
            or_(
                Article.name == name,
                Article.code == code
            )
        ).count()
        if same_articles_count:
            raise UniqueFailed(message='Статья с таким именем или кодом уже существует')

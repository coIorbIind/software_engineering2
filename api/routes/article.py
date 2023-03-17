from typing import Optional

from fastapi import Query
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from fastapi_filter import FilterDepends
from sqlalchemy import or_
from starlette.responses import Response
from starlette.status import HTTP_204_NO_CONTENT

from db import Article, Tag, ArticleTag
from api.routes.base import BaseRoute
from api.schemas.article import (
    ArticleListSchema,
    ArticleCreateSchema,
    ArticlePutSchema,
    ArticlePatchSchema,
)
from api.schemas.base import PaginatedResponse, LimitOffsetPaginationSchema
from crud.article import (
    get_article_by_code_or_404,
    create_article,
    ArticleFilter,
    get_articles,
    patch_article,
)
from logic.execptions import UniqueFailed
from logic.pagination import LimitOffsetPagination


router = InferringRouter()


@cbv(router)
class ArticleRoute(BaseRoute):
    model = Article
    joined_load = ('tags', )
    paginator = LimitOffsetPagination()

    @router.get('/{code}')
    def get_article(self, code: str) -> ArticleListSchema:
        """ Получение статьи по её коду """
        article = get_article_by_code_or_404(session=self.session, code=code, joined_load=self.joined_load)
        article.tags = sorted(article.tags, key=lambda tag: tag.name)
        return article

    @router.post('/')
    def create(self, article: ArticleCreateSchema) -> ArticleListSchema:
        """ Создание статьи """
        self._validate_name_and_code(code=article.code, name=article.name)
        return create_article(self.session, article)

    @router.get('/')
    def list(
            self,
            tag_codes: Optional[list[str]] = Query(default=None),
            filter_obj: ArticleFilter = FilterDepends(ArticleFilter),
            limit: int = 5,
            offset: int = 0
    ) -> PaginatedResponse:
        """ Получение списка статей """
        articles = get_articles(self.session, filter_obj, joined_load=self.joined_load)
        if tag_codes:
            articles = articles.join(ArticleTag).join(Tag).filter(Tag.code.in_(tag_codes))
        total = articles.count()
        articles = self.session.execute(self.paginator.paginate(articles, limit, offset)).scalars().all()
        for article in articles:
            article.tags = sorted(article.tags, key=lambda tag: tag.name)
        return PaginatedResponse(
            data=articles,
            pagination=LimitOffsetPaginationSchema(limit=limit, offset=offset, total=total)
        )

    @router.put('/{code}')
    def put_article(self, code: str, article: ArticlePutSchema) -> ArticleListSchema:
        """ Создание статьи """
        db_obj = get_article_by_code_or_404(session=self.session, code=code, joined_load=self.joined_load)
        self._validate_name_and_code(code=article.code, name=article.name)
        return patch_article(self.session, obj=db_obj, schema=article)

    @router.patch('/{code}')
    def patch_article(self, code: str, article: ArticlePatchSchema) -> ArticleListSchema:
        """ Создание статьи """
        db_obj = get_article_by_code_or_404(session=self.session, code=code, joined_load=self.joined_load)
        self._validate_name_and_code(code=article.code, name=article.name)
        return patch_article(self.session, obj=db_obj, schema=article)

    @router.delete('/{code}')
    def delete_article(self, code: str):
        """ Получение статьи по её коду """
        article = get_article_by_code_or_404(session=self.session, code=code, joined_load=self.joined_load)
        (
            self.session.query(Article)
            .filter(
                Article.id == article.id
            ).delete()
        )

        return Response(status_code=HTTP_204_NO_CONTENT)

    def _validate_name_and_code(self, code: str, name: str):
        """ Проверка уникальности имени и кода статьи """
        same_articles_count = self.session.query(Article).filter(
            or_(
                Article.name == name,
                Article.code == code
            )
        ).count()
        if same_articles_count:
            raise UniqueFailed(message='Статья с таким именем или кодом уже существует')

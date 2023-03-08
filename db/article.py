from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from db.base import Base


class ArticleTag(Base):
    __tablename__ = 'article_tags'
    id = Column(Integer, name='id', primary_key=True, autoincrement=True, index=True)
    article_id = Column(Integer, ForeignKey('article.id', ondelete='CASCADE'))
    article = relationship('Article', overlaps='article_tags,tags')
    tag_id = Column(Integer, ForeignKey('tag.id', ondelete='CASCADE'))
    tag = relationship('Tag', overlaps='article_tags,tags')


class Article(Base):
    __tablename__ = 'article'

    id = Column(Integer, name='id', primary_key=True, autoincrement=True, index=True)
    name = Column(String, name='name', nullable=False, index=True, unique=True)
    code = Column(String, name='code', nullable=False, index=True, unique=True)
    content = Column(String, name='content', nullable=False)
    created_at = Column(DateTime, name='created_at', nullable=False)
    author = Column(String, name='author', nullable=True, index=True)
    tags = relationship('Tag', secondary='article_tags')

    def __str__(self):
        return f'Article: {self.name}'

    def __repr__(self):
        return f'Article: {self.name}'

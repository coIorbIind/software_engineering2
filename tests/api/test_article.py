import pytest

from db import Article


@pytest.mark.parametrize('correct', [True, False])
def test_get_article(client, article_factory, correct):
    article = article_factory()
    path = f'/api/v1/posts/{article.code}'
    status_code = 200
    if not correct:
        path += '_extra'
        status_code = 404

    response = client.get(path)
    assert response.status_code == status_code
    if correct:
        assert response.json()['name'] == article.name


def test_create_article(client, tag_factory, scope_session):
    tags = [tag_factory(), tag_factory()]
    data = {
        'name': 'name',
        'code': 'code',
        'author': 'author',
        'content': 'content',
        'tags': [tag.code for tag in tags]
    }
    response = client.post('/api/v1/posts/', json=data)
    assert response.status_code == 200
    articles = scope_session.query(Article)
    assert articles.count() == 1
    article = articles.first()
    assert article.name == data['name']
    assert article.tags == tags


@pytest.mark.parametrize('error', ['name', 'code'])
def test_unique_in_create_article(client, article_factory, scope_session, error):
    if error == 'name':
        article_factory(name='name')
    elif error == 'code':
        article_factory(code='code')
    data = {
        'name': 'name',
        'code': 'code',
        'author': 'author',
        'content': 'content',
    }
    response = client.post('/api/v1/posts/', json=data)
    assert response.status_code == 400


@pytest.mark.parametrize('limit, offset, length', [(None, 0, 5), (5, 0, 5), (5, 1, 4)])
def test_articles_pagination(client, article_factory, limit, offset, length):
    articles = [article_factory() for _ in range(5)]
    q = ''
    if limit or offset:
        q = f'?limit={limit}&offset={offset}'
    response = client.get('/api/v1/posts/' + q)
    assert response.status_code == 200
    data = response.json()

    assert len(data) == length
    assert all([data[i]['name'] == articles[offset + i].name for i in range(length)])


def test_tags_sorting(client, article_factory, tag_factory, article_tag_factory):
    last_tag = tag_factory(name='zname')
    first_tag = tag_factory(name='aname')
    article = article_factory()
    article_tag_factory(article=article, tag=last_tag)
    article_tag_factory(article=article, tag=first_tag)

    response = client.get('/api/v1/posts/')
    assert response.status_code == 200
    data = response.json()[0]
    assert data['tags'][0]['name'] == first_tag.name
    assert data['tags'][1]['name'] == last_tag.name


@pytest.mark.parametrize('with_name', [True, False])
@pytest.mark.parametrize('with_code', [True, False])
@pytest.mark.parametrize('with_tags', [True, False])
def test_articles_filter(
    client, article_factory, tag_factory, article_tag_factory,
    with_code, with_name, with_tags
):
    tag1 = tag_factory()
    tag2 = tag_factory()
    article_by_name_and_code = article_factory(name='name', code='code')
    article_tag_factory(article=article_by_name_and_code, tag=tag1)

    article_by_to_tags = article_factory()
    article_tag_factory(article=article_by_to_tags, tag=tag2)

    q = '?'
    if with_name:
        q += 'names=name&'
    if with_code:
        q += 'codes=code&'
    if with_tags:
        q += f'tag_codes={tag1.code}&tag_codes={tag2.code}'
    response = client.get('/api/v1/posts/' + q)
    assert response.status_code == 200
    data = response.json()
    if with_name or with_code:
        assert len(data) == 1
        assert data[0]['name'] == article_by_name_and_code.name
    else:
        assert len(data) == 2
        assert {item['name'] for item in data} == {article_by_name_and_code.name, article_by_to_tags.name}

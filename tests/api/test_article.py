import pytest


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

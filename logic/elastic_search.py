import requests

from db.article import Article
from .logger import init_logger
from .execptions import SearchError


logger = init_logger(__name__)


def create_index():
    response = requests.put(
        url='http://elastic_search:9200/article',
        json={
            'settings': {'number_of_shards': 1},
            'mappings': {
                'properties': {
                    'id': {'type': 'integer'},
                    'code': {'type': 'text'},
                    'name': {'type': 'text'},
                    'content': {'type': 'text'},
                    'author': {'type': 'text'},
                }
            }
        },
        verify=False,
        cert=False,
        headers={'User-Agent': 'PostmanRuntime/7.32.2'}
    )

    logger.info(
        f'Create index. Status: {response.status_code}; Result: {response.json()}'
    )


def create_document(article: Article):

    response = requests.post(
        url='http://elastic_search:9200/article/_doc/',
        json={
            'id': article.id,
            'code': article.code,
            'name': article.name,
            'content': article.content,
            'author': article.author,
        },
        verify=False,
        cert=False,
        headers={'User-Agent': 'PostmanRuntime/7.32.2'}
    )
    logger.info(
        f'Create document for {article.name}. Status: {response.status_code}; Result: {response.json()}'
    )


def search_document(filters: dict, limit: int = 5, offset: int = 0) -> list[int]:
    if not filters:
        query = {'match_all': {}}
    else:
        query = {'match': filters}
    response = requests.post(
        url='http://elastic_search:9200/article/_search/',
        json={
            'from': offset,
            'size': limit,
            'query': query
        },
        verify=False,
        cert=False,
        headers={'User-Agent': 'PostmanRuntime/7.32.2'}
    )
    logger.info(
        f'Search for {filters}. Status: {response.status_code}; Result: {response.json()}'
    )
    if response.status_code == 200:
        ids = [item['_source']['id'] for item in response.json()['hits']['hits']]
        return ids

    else:
        raise SearchError

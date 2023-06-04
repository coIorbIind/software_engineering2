from fastapi import Request
from fastapi.responses import JSONResponse


class BaseAPIException(Exception):
    """ Базовое исключение """
    status_code = 500
    code = 'exception'
    message = 'Ошибка!'

    def __init__(self, loc=None, **kwargs):
        self.context = kwargs
        self.loc = [['body'] + location for location in loc] if loc else [['body']]

    def to_json(self):
        return {
            'code': self.code,
            'context': self.context,
            'detail': [
                {
                    'location': loc,
                    'message': self.context.get('message', self.message)
                } for loc in self.loc
            ]
        }


class ObjectNotFound(BaseAPIException):
    """ Объект не найден """
    status_code = 404
    code = 'object_not_fount'
    message = 'Объект не найден'


class UniqueFailed(BaseAPIException):
    """ Нарушена уникальность поля """
    status_code = 400
    code = 'unique constraint failed'
    message = 'Нарушена уникальность поля'


class SearchError(BaseAPIException):
    """ Ошибка при поиске в elastic_search """
    status_code = 400
    code = 'search error'
    message = 'Ошибка при поиске в elastic_search'


class ConsoleError(Exception):
    """ Ошибка при вызове консольной команды """
    pass


def exception_handler(request: Request, exception: BaseAPIException) -> JSONResponse:
    """ Перевод исключения в json """
    return JSONResponse(
        status_code=exception.status_code,
        content=exception.to_json()
    )

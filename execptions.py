from fastapi import Request
from fastapi.responses import JSONResponse


class BaseAPIException(Exception):
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
    status_code = 404
    code = 'object_not_fount'
    message = 'Объект не найден'


class UniqueFailed(BaseAPIException):
    status_code = 400
    code = 'unique constraint failed'
    message = 'Нарушена уникальность поля'


class ConsoleError(Exception):
    pass


def exception_handler(request: Request, exception: BaseAPIException) -> JSONResponse:
    return JSONResponse(
        status_code=exception.status_code,
        content=exception.to_json()
    )

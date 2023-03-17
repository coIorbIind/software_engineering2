from sqlalchemy.orm import Query


class LimitOffsetPagination:
    """ Limit, Offset пагинация """
    def paginate(self, query: Query, limit: int = 5, offset: int = 0) -> Query:
        return query.offset(offset).limit(limit)

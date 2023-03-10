import os


class Settings:
    DB_USER = 'postgres'
    USER_PASSWORD = 1234
    DB_NAME = 'database'
    HOST = 'localhost'

    @property
    def database_url(self) -> str:
        db_user = os.getenv('DB_USER', self.DB_USER)
        user_password = os.getenv('USER_PASSWORD', self.USER_PASSWORD)
        db_name = os.getenv('DB_NAME', self.DB_NAME)
        host = os.getenv('HOST', self.HOST)
        port = os.getenv('PORT', 5432)

        return f'postgresql+psycopg2://{db_user}:{user_password}@{host}:{port}/{db_name}'


settings = Settings()

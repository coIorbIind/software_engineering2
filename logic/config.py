import os


class Settings:
    DB_USER = 'test_user'
    USER_PASSWORD = 1234
    DB_NAME = 'testing_db'
    HOST = 'localhost'

    @property
    def database_url(self) -> str:
        db_user = os.getenv('DB_USER', self.DB_USER)
        user_password = os.getenv('USER_PASSWORD', self.USER_PASSWORD)
        db_name = os.getenv('DB_NAME', self.DB_NAME)
        host = os.getenv('HOST', self.HOST)

        return f'postgresql+psycopg2://{db_user}:{user_password}@{host}:5432/{db_name}'


settings = Settings()

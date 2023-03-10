import os

from logic.config import Settings as BaseSettings


class Settings(BaseSettings):

    @property
    def database_url(self) -> str:
        db_user = os.getenv('TEST_DB_USER', self.DB_USER)
        user_password = os.getenv('TEST_USER_PASSWORD', self.USER_PASSWORD)
        host = os.getenv('TEST_HOST', self.HOST)
        port = os.getenv('TEST_PORT', 5433)
        db_name = os.getenv('TEST_DB_NAME', self.DB_NAME)

        return f'postgresql+psycopg2://{db_user}:{user_password}@{host}:{port}/{db_name}'


settings = Settings()

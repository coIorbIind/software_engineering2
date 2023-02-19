import os


class Settings:

    @property
    def database_url(self) -> str:
        db_user = os.getenv('DB_USER')
        user_password = os.getenv('USER_PASSWORD')
        db_name = os.getenv('DB_NAME')
        host = os.getenv('HOST')

        return f'postgresql+psycopg2://{db_user}:{user_password}@{host}/{db_name}'


settings = Settings()
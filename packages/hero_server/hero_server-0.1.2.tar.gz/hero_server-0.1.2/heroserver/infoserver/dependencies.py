import os

from fastapi import HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi_mail import ConnectionConfig, FastMail
from infoserver.db import DB
from infoserver.dbmem import DBMem
from jwt import PyJWTError
from pydantic_settings import BaseSettings
from web.auth import JWTHandler


class Settings(BaseSettings):
    JWT_SECRET_KEY: str = os.getenv('JWT_SECRET_KEY')
    MAIL_USERNAME: str = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD: str = os.getenv('MAIL_PASSWORD')
    MAIL_FROM: str = os.getenv('MAIL_FROM')
    MAIL_PORT: int = int(os.getenv('MAIL_PORT', 587))
    MAIL_SERVER: str = os.getenv('MAIL_SERVER')
    SERVERHOST: str = os.getenv('SERVERHOST', 'http://localhost:8000')

    class Config:
        env_file = '.env'


class Dependencies:
    def __init__(
        self,
        db_path: str,
        templates_dir: str,
        static_dir: str,
        static_dir2: str,
        hero_web_dir: str,
        collections_dir: str,
        serverhost: str,
    ):
        print('INITIALIZING DEPENDENCIES')
        self.settings = Settings()
        self.db_path = db_path
        self.templates_dir = templates_dir
        self.static_dir = static_dir
        self.static_dir2 = static_dir2
        self.hero_web_dir = hero_web_dir
        self.collections_dir = collections_dir
        self.serverhost = serverhost

        self.jwt_handler = JWTHandler()

        # Check that all required settings are filled in
        required_settings = [
            self.settings.JWT_SECRET_KEY,
            self.settings.MAIL_USERNAME,
            self.settings.MAIL_PASSWORD,
            self.settings.MAIL_FROM,
            self.settings.MAIL_PORT,
            self.settings.MAIL_SERVER,
        ]
        if not all(required_settings):
            raise ValueError('Some required settings are missing')

        # Email configuration
        self.conf = ConnectionConfig(
            MAIL_USERNAME=self.settings.MAIL_USERNAME,
            MAIL_PASSWORD=self.settings.MAIL_PASSWORD,
            MAIL_FROM=self.settings.MAIL_FROM,
            MAIL_PORT=self.settings.MAIL_PORT,
            MAIL_SERVER=self.settings.MAIL_SERVER,
            MAIL_STARTTLS=True,
            MAIL_SSL_TLS=False,
            USE_CREDENTIALS=True,
        )

        # Jinja2 templates for rendering HTML
        self.templates = Jinja2Templates(directory=self.templates_dir)

        # Initialize DB
        self.db = DB(self.db_path, reset=False)

    def get_dbmem(self, request: Request):
        if not hasattr(request.state, 'dbmem'):
            print('CACHE MISS DBMEM')
            token = request.cookies.get('access_token')
            if not token:
                raise HTTPException(status_code=401, detail='Not authenticated')
            try:
                user_email = self.jwt_handler.verify_access_token(token)
            except PyJWTError:
                return HTTPException(
                    status_code=401,
                    detail='Not authenticated, email verification',
                )
            request.session['user_email'] = user_email
            request.state.dbmem = DBMem(self.db, user_email)
        return request.state.dbmem

    def get_fastmail(self):
        return FastMail(self.conf)

    def get_templates(self):
        return self.templates

    def get_jwt_handler(self):
        return self.jwt_handler

    def get_db(self):
        return self.db

    def get_static_dir(self):
        return self.static_dir

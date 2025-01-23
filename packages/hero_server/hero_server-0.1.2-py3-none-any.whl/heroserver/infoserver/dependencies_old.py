import os

from fastapi import HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi_mail import ConnectionConfig, FastMail
from infoserver.db import DB
from infoserver.dbmem import DBMem
from jwt import PyJWTError
from web.auth import JWTHandler

# Initialize JWTHandler
jwt_handler = JWTHandler()

# Email configuration
conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv('MAIL_USERNAME'),
    MAIL_PASSWORD=os.getenv('MAIL_PASSWORD'),
    MAIL_FROM=os.getenv('MAIL_FROM'),
    MAIL_PORT=int(os.getenv('MAIL_PORT', 587)),
    MAIL_SERVER=os.getenv('MAIL_SERVER'),
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
)

# Check if all required environment variables are set
required_env_vars = [
    'MAIL_USERNAME',
    'MAIL_PASSWORD',
    'MAIL_FROM',
    'MAIL_PORT',
    'MAIL_SERVER',
    'JWT_SECRET_KEY',
]
missing_vars = [var for var in required_env_vars if not os.getenv(var)]

if missing_vars:
    raise EnvironmentError(
        f"Missing required environment variables: {', '.join(missing_vars)}"
    )

# Jinja2 templates for rendering HTML
templates = Jinja2Templates(directory='templates')

# Initialize DB
db = DB(
    '~/code/git.ourworld.tf/freeflowuniverse/heroweb/authdb_example',
    reset=False,
)


# Dependency to get DBMem for each request
def get_dbmem(request: Request):
    if not hasattr(request.state, 'dbmem'):
        print('CACHE MISS DBMEM')
        jwt_handler = get_jwt_handler()
        token = request.cookies.get('access_token')
        if not token:
            raise HTTPException(status_code=401, detail='Not authenticated')
        try:
            user_email = jwt_handler.verify_access_token(token)
        except PyJWTError:
            # raise HTTPException(status_code=401, detail="Invalid token")
            return HTTPException(
                status_code=401, detail='Not authenticated, email verification'
            )
        request.session.set('user_email', user_email)
        request.state.dbmem = DBMem(db, user_email)
    return request.state.dbmem


# Function to get FastMail
def get_fastmail():
    return FastMail(conf)


# Make these dependencies available
def get_templates():
    return templates


def get_jwt_handler():
    return jwt_handler


def get_db():
    return db

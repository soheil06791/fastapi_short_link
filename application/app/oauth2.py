import base64
from typing import List
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel

from config.config import settings
from utils.utils import read_and_encode_file
import os
file_path = os.path.split(os.path.abspath(__file__))[0]

class Settings(BaseModel):
    authjwt_algorithm: str = settings.JWT_ALGORITHM
    authjwt_decode_algorithms: List[str] = [settings.JWT_ALGORITHM]
    authjwt_token_location: set = {'cookies', 'headers'}
    authjwt_access_cookie_key: str = 'access_token'
    authjwt_refresh_cookie_key: str = 'refresh_token'
    authjwt_cookie_csrf_protect: bool = False
    authjwt_public_key: str = read_and_encode_file(f"{file_path}/../{settings.JWT_PUBLIC_KEY}")
    authjwt_private_key: str = read_and_encode_file(f"{file_path}/../{settings.JWT_PRIVATE_KEY}")


@AuthJWT.load_config
def get_config():
    return Settings()

from fastapi import APIRouter, status, Depends, HTTPException, responses, Response
from fastapi import Query, Body, Header, Request
from fastapi.encoders import jsonable_encoder
from datetime import timedelta
from app.schemas import *
from app.oauth2 import AuthJWT
from utils.db_manager import execute
from utils.query_manger import *
from config.config import settings
from utils.utils import *
from pydantic import HttpUrl
import uuid

router = APIRouter()
ACCESS_TOKEN_EXPIRES_IN = settings.ACCESS_TOKEN_EXPIRES_IN
REFRESH_TOKEN_EXPIRES_IN = settings.REFRESH_TOKEN_EXPIRES_IN


@router.post('/register', status_code=status.HTTP_201_CREATED, response_model=CreateUserSchema)
async def create_user(payload: CreateUserSchema = Depends()):
    try:
        exist_user = await execute(check_by_email, [payload.email])
        
        if exist_user:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Account already exist")
        if payload.password != payload.passwordConfirm:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password not match")
        payload.password = hash_password(payload.password)
        payload.role = 'user'
        payload.verified = True
        run_query = await execute(new_user, list(payload.dict(exclude={'passwordConfirm'}).values()))
        if run_query == 'error':
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Query Error")
        return responses.JSONResponse(payload.dict(exclude = {'password', 'passwordConfirm'}))
    except Exception as e:
        error = e.__class__.__name__
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error)


@router.post('/login', status_code=status.HTTP_200_OK, tags = ['User'])
async def login(response: Response, payload: LoginUserSchema = Depends(), Authorize: AuthJWT = Depends()):
    try:

        user = await execute(get_user_info, [payload.email])
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found")
        user = user[0]
        if not user['verified']:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email Not Verified")
        if not verify_password(payload.password, user['password']):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect Password")
        
        subject = encode_crypto(user['id'], settings.KEY_TOKEN)
        access_token = Authorize.create_access_token(subject, expires_time=timedelta(minutes=ACCESS_TOKEN_EXPIRES_IN))
        refresh_token = Authorize.create_refresh_token(subject, expires_time=timedelta(minutes=ACCESS_TOKEN_EXPIRES_IN))
        
        response.set_cookie('access_token', access_token, ACCESS_TOKEN_EXPIRES_IN * 60,
                            ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, True, 'lax')
        response.set_cookie('refresh_token', refresh_token,
                            REFRESH_TOKEN_EXPIRES_IN * 60, REFRESH_TOKEN_EXPIRES_IN * 60, '/', None, False, True, 'lax')
        response.set_cookie('logged_in', 'True', ACCESS_TOKEN_EXPIRES_IN * 60,
                            ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, False, 'lax')
        return {'status': 'success', 'access_token': access_token}
    except Exception as e:
        error = e.__class__.__name__
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error)

@router.post('/urls', status_code = status.HTTP_201_CREATED, response_model= AddUrlResponse, tags = ['User'])
async def add_new_link(url: HttpUrl ,Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
        token = Authorize.get_jwt_subject()
        if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= "UnAuthorized")
        user_id = int(decode_crypto(token, settings.KEY_TOKEN))
        exist_user = await execute(check_by_uid, [user_id])
        if not exist_user:
            raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail= "user not exist")
        short_link = uuid.uuid4().hex[:10]
        await execute(add_new_link, [user_id, url, short_link])
        return AddUrlResponse(short_link=f"{settings.DOMAIN}/{short_link}")
    except Exception as e:
        error = e.__class__.__name__
        if error == 'MissingTokenError':
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = "Refresh Token")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error)

@router.get('/urls', status_code = status.HTTP_200_OK, response_model = list[UrlResponse], tags = ['User'])
async def user_links(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
        token = Authorize.get_jwt_subject()
        if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= "UnAuthorized")
        user_id = int(decode_crypto(token, settings.KEY_TOKEN))
        exist_user = await execute(check_by_uid, [user_id])
        if not exist_user:
            raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail= "user not exist")
        user_links = await execute(get_user_links, [user_id])
        for link in user_links:
            link['short_url'] = f"{settings.DOMAIN}/{link.pop('short_link')}"
        return user_links
    except Exception as e:
        error = e.__class__.__name__
        if error == 'MissingTokenError':
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = "Refresh Token")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error)

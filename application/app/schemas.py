from pydantic import BaseModel, EmailStr, constr, Field, HttpUrl, validator
from fastapi import HTTPException, status
from typing import Hashable
from datetime import datetime
from uuid import UUID
from enum import Enum


class UserBaseSchema(BaseModel):
    name: str
    email: EmailStr


class UserType(str, Enum):
    admin = "admin"
    user = "user"


class CreateUserSchema(UserBaseSchema):
    password: constr(min_length=8, max_length=32, regex="^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)[a-zA-Z\\d]*$")
    passwordConfirm: str
    role: UserType = UserType.user
    verified: bool = False
    
    @validator('role')
    def validate_role(cls, v, values):
        if values['email'] not in ['soheil@gmail.com', 'soheil1991@gmail.com'] and v.value == 'admin':
            raise HTTPException(detail = "access denied", status_code = status.HTTP_403_FORBIDDEN)
    
    @validator('verified')
    def validate_verified(cls, v, values):
        if values['email'] not in ['soheil@gmail.com', 'soheil1991@gmail.com'] and v == True:
            raise HTTPException(detail = "access denied", status_code = status.HTTP_403_FORBIDDEN)


class LoginUserSchema(BaseModel):
    email: EmailStr
    password: constr(min_length=8)



class UrlResponse(BaseModel):
    url: HttpUrl
    short_url: str
    view: int


class AddUrlResponse(BaseModel):
    short_link: HttpUrl
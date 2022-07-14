import email
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint



class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config: # This is used to convert to dict
        orm_mode = True


class Post(PostBase): # Extending to PostBase gives back title, content, published
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config: # This is used to convert to dict
        orm_mode = True


class PostOut(BaseModel):
    Post: Post  # Referencing the Post class
    votes: int
    class Config: # This is used to convert to dict
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)  # takes integers less or equal to 1 (le=1), dir is used to vote if 1, to delete if 0
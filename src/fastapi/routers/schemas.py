from datetime import datetime

from pydantic import BaseModel


class UserPass(BaseModel):
    username: str
    password: str


class UserInfo(BaseModel):
    id: str
    username: str
    created_at: datetime

    class Config:
        orm_mode = True

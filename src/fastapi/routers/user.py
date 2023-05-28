from fastapi import APIRouter, Depends

from .schemas import UserInfo
from .utils import authorize_user
from models import User


router = APIRouter(prefix="/user")


@router.get("/")
def get_user(user: User = Depends(authorize_user)):
    return UserInfo.from_orm(user)

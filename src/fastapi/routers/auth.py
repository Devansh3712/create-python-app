import logging
from datetime import datetime, timedelta

import jwt
from fastapi import status, APIRouter, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import Session

from .schemas import UserPass
from config import settings
from models import engine, User


router = APIRouter()


@router.post("/signup", status_code=status.HTTP_201_CREATED)
def new_user(_user: UserPass):
    try:
        with Session(engine) as session:
            user = User(_user.username, _user.password)
            session.add(user)
            session.commit()
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists"
        )
    except Exception as error:
        logging.error(error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Server error"
        )


@router.get("/login")
def user_token(_user: UserPass):
    try:
        with Session(engine) as session:
            user = session.query(User).filter_by(username=_user.username).one()
            if not user.verify_password(_user.password):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Incorrect password",
                )
            payload = {
                "exp": datetime.utcnow() + timedelta(seconds=3600),
                "id": user.id,
            }
            token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
            return JSONResponse({"token": token})
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    except Exception as error:
        logging.error(error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Server error"
        )

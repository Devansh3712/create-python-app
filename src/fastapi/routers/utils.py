import logging

import jwt
from fastapi import status, HTTPException, Request
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from config import settings
from models import engine, User


def authorize_user(request: Request) -> User:
    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization token not found",
        )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms="HS256")
        with Session(engine) as session:
            user = session.query(User).filter_by(id=payload.get("id")).one()
            return user
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization token expired",
        )
    except InvalidSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization token",
        )
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    except Exception as error:
        logging.error(error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Server error"
        )

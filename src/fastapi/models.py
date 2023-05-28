from datetime import datetime
from uuid import uuid4

import bcrypt
from sqlalchemy import create_engine, Column, DateTime, String
from sqlalchemy.orm import declarative_base

from config import settings


def create_id() -> str:
    return uuid4().hex.replace("-", "")


Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column("id", String, primary_key=True, index=True)
    username = Column("username", String, unique=True)
    password = Column("password", String)
    created_at = Column("created_at", DateTime)

    def __init__(self, username: str, password: str) -> None:
        self.id = create_id()
        self.username = username
        self.password = bcrypt.hashpw(
            password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")
        self.created_at = datetime.now()

    def __repr__(self):
        return f"User(id={self.id}, username={self.username}, password={self.password}, created_at={self.created_at})"

    def verify_password(self, password: str):
        return bcrypt.checkpw(password.encode("utf-8"), self.password.encode("utf-8"))


engine = create_engine(settings.DATABASE_URI, echo=False)

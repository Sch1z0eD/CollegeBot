from datetime import datetime

from sqlalchemy import Integer, Column, Boolean, ForeignKey, String, DateTime, Date, Time, func
from sqlalchemy.ext.declarative import declarative_base

from bot.database.role import UserRole

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(Integer, unique=True)
    role = Column(String(), default=UserRole.USER.value)
    created_at = Column(DateTime(True), server_default=func.now())


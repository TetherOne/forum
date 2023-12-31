import datetime
from typing import Annotated

import pytz
from flask_login import UserMixin

from sqlalchemy import ForeignKey, text, func, Column, DateTime

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


int_pk = Annotated[int, mapped_column(primary_key=True)]



def utcnow():
    return datetime.datetime.now(pytz.timezone('Etc/GMT-5'))



class Base(DeclarativeBase):
    id: Mapped[int_pk]
    created_at: Mapped[datetime] = Column(DateTime, default=utcnow)



class User(Base, UserMixin):
    """

    Модель пользователя

    """
    __tablename__ = 'users'


    username: Mapped[str]
    email: Mapped[str]
    password: Mapped[str]


    articles: Mapped[list['Article']] = relationship(
        back_populates='user',
        cascade='all'
    )



class Article(Base):
    """

    Модель статьи

    """
    __tablename__ = 'articles'


    name_of_article: Mapped[str]
    text_of_article: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped['User'] = relationship(back_populates='articles')


    categories: Mapped[list['Category']] = relationship(
        back_populates='article',
        cascade='all',
    )



class Category(Base):
    """

    Модель категорий объявлений

    """
    __tablename__ = 'categories'

    name_of_category: Mapped[str]
    article_id: Mapped[int] = mapped_column(ForeignKey('articles.id'))
    article: Mapped['Article'] = relationship(back_populates='categories')





















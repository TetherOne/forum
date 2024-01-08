import datetime

from typing import Annotated, Optional

from flask_login import UserMixin

from sqlalchemy import ForeignKey, String
from sqlalchemy import Column
from sqlalchemy import DateTime

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from views.models_view.utc_now_view import utcnow



int_pk = Annotated[int, mapped_column(primary_key=True)]



class Base(DeclarativeBase):
    """

    Родительский класс,
    имеет атрибуты id (primary_key=True),
    created_at (default=utcnow)

    """
    id: Mapped[int_pk]
    created_at: Mapped[datetime] = Column(DateTime, default=utcnow)



class User(Base, UserMixin):
    """

    Модель пользователя:

    id: int
    username: str
    email: str
    password: str
    created_at: datetime

    """
    __tablename__ = 'users'


    username: Mapped[str]
    avatar: Mapped[Optional[str]] = Column(String)
    email: Mapped[str]
    password: Mapped[str]


    articles: Mapped[list['Article']] = relationship(
        back_populates='user',
        cascade='all'
    )



class Article(Base):
    """

    Модель статьи:

    id: int, primary_key
    name_of_article: str
    text_of_article: str
    user_id: int, Foreignkey
    created_at: datetime

    """
    __tablename__ = 'articles'


    name_of_article: Mapped[str]
    category: Mapped[str]
    text_of_article: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped['User'] = relationship(back_populates='articles')

    images: Mapped[list['Image']] = relationship(
        back_populates='article',
        cascade='all'
    )


















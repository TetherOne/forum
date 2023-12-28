from flask_login import UserMixin
from sqlalchemy import ForeignKey

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship



class Base(DeclarativeBase):
    pass



class User(Base, UserMixin):
    """

    Модель пользователя

    """
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
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

    id: Mapped[int] = mapped_column(primary_key=True)
    name_of_article: Mapped[str]
    category: Mapped[str]
    text_of_article: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped['User'] = relationship(back_populates='articles')

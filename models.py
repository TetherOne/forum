from views.model_views.utc_now_view import utcnow

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped

from flask_login import UserMixin

from sqlalchemy import ForeignKey
from sqlalchemy import DateTime
from sqlalchemy import String
from sqlalchemy import Column

from typing import Annotated
from typing import Optional

import datetime



int_pk = Annotated[int, mapped_column(primary_key=True)]



class Base(DeclarativeBase):

    id: Mapped[int_pk]
    created_at: Mapped[datetime] = Column(DateTime, default=utcnow)



class User(Base, UserMixin):

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

    __tablename__ = 'articles'

    name_of_article: Mapped[str]
    category: Mapped[str]
    text_of_article: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped['User'] = relationship(back_populates='articles')
















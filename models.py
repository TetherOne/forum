from sqlalchemy import create_engine
from sqlalchemy import ForeignKey

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker




engine = create_engine(url='sqlite:///./db.sqlite3')
session = sessionmaker()
session.configure(bind=engine)



class Base(DeclarativeBase):
    pass



class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    age: Mapped[int]
    surname: Mapped[str]
    username: Mapped[str]

    articles: Mapped[list['articles']] = relationship(
        back_populates='user',
        cascade='all'
    )



class Article(Base):
    __tablename__ = 'article'

    id: Mapped[int] = mapped_column(primary_key=True)
    category: Mapped[str]
    name_of_article: Mapped[str]
    text_of_article: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    user: Mapped['User'] = relationship(back_populates='articles')

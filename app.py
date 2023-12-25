from datetime import datetime
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column, sessionmaker, Session
from sqlalchemy import ForeignKey, create_engine

from models import Base

app = Flask(__name__)

engine = create_engine(url='sqlite:///./db.sqlite3')
session = sessionmaker()
session.configure(bind=engine)



def main():
    Base.metadata.create_all(bind=engine)
    with Session(engine) as session:
        session.commit()



if __name__ == '__main__':
    app.run()
    main()

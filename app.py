from flask import Flask, render_template

from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from models import Base




app = Flask(__name__)

engine = create_engine(url='sqlite:///./db.sqlite3')
session = sessionmaker()
session.configure(bind=engine)


@app.route('/', methods=['GET'])
def main_page():
    """
    Функция для отрисовки главной страницы сайта
    """
    return render_template('forum/main_page.html')



@app.route('/register/', methods=['GET'])
def register_page():
    """
    Функция для отрисовки страницы регистрации сайта
    """
    return render_template('auth/register.html')



@app.route('/login/', methods=['GET'])
def login_page():
    """
    Функция для отрисовки страницы входа на сайт
    """
    return render_template('auth/login.html')



def main():
    Base.metadata.create_all(bind=engine)
    with Session(engine) as session:
        session.commit()



if __name__ == '__main__':
    app.run(debug=True)
    main()

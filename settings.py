from flask import Flask

from flask_restful import Api

from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker



app = Flask(__name__)
api = Api(app)



engine = create_engine('postgresql://postgres:qwerty@localhost:5432/forum')
app.config['SECRET_KEY'] = 'forum'
SessionFactory = sessionmaker(bind=engine)
from flasgger import Swagger
from flask import Flask

from flask_restful import Api

from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker

from swagger_settings import swagger_template

app = Flask(__name__)
api = Api(app)



swagger_config = {
    "swagger": "2.0",
    "info": {
        "title": "Forum API",
        "version": "1.0"
    },
}


Swagger(app, template=swagger_template)


engine = create_engine('postgresql://postgres:qwerty@localhost:5432/forum')
app.config['SECRET_KEY'] = 'forum'
SessionFactory = sessionmaker(bind=engine)


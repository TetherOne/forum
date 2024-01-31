from swagger_settings import swagger_template

from sqlalchemy.orm import sessionmaker

from sqlalchemy import create_engine

from flask_caching import Cache

from flask_restful import Api

from flasgger import Swagger

from flask import Flask



app = Flask(__name__)
api = Api(app)
cache = Cache(app, config={'CACHE_TYPE': 'redis', 'CACHE_KEY_PREFIX': 'flask_cache', 'CACHE_REDIS_URL': 'redis://127.0.0.1:6379'})



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


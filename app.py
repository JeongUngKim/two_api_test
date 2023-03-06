from flask import Flask
from flask_restful import Api
from config import Config
from flask_jwt_extended import JWTManager

from resource.content import search


app = Flask(__name__)

app.config.from_object(Config)

jwt = JWTManager(app)

api = Api(app)
api.add_resource(search,'/search')
if __name__ == '__main__' : 
    app.run()

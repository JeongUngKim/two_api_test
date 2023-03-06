from flask import Flask
from flask_restful import Api
from config import Config
from flask_jwt_extended import JWTManager

from resource.content import contentLike, contentReview, search
from resource.user import UserContentLike, UserIspassword, UserLoginResource, UserLogoutResource, UserPasswordChanged, UserRegisterResource


app = Flask(__name__)

app.config.from_object(Config)

jwt = JWTManager(app)

api = Api(app)

# 검색 api
api.add_resource(search,'/search')

# 컨텐츠 찜관련 api
api.add_resource(contentLike,'/contentlike/<int:contentId>')
api.add_resource(contentReview,'/review/<int:contentId>')


# 유저 로그인관련 api
api.add_resource(UserRegisterResource,"/register")
api.add_resource(UserLoginResource,"/login")
api.add_resource(UserLogoutResource,"/logout")
api.add_resource(UserIspassword,"/isregister")
api.add_resource(UserPasswordChanged,"/changedpassword")

# 유저 정보 관련 api
api.add_resource(UserContentLike,'/contentlike/me')

if __name__ == '__main__' : 
    app.run()

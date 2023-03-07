from flask import Flask
from flask_restful import Api
from config import Config
from flask_jwt_extended import JWTManager

from resource.content import contentLike, contentReview, contentReviewUD, search
from resource.user import UserContentLike, UserIsEmail, UserIsId, UserIsNickname, UserIspassword, UserLoginResource, UserLogoutResource, UserPasswordChanged, UserRegisterResource


app = Flask(__name__)

app.config.from_object(Config)

jwt = JWTManager(app)

api = Api(app)

# 검색 api
api.add_resource(search,'/search')

# 컨텐츠 찜관련 api
api.add_resource(contentLike,'/contentlike/<int:contentId>')

# 컨텐츠 리뷰 관련 api
api.add_resource(contentReview,'/content/<int:contentId>/review')
api.add_resource(contentReviewUD,'/content/<int:contentId>/review/<int:contentReviewId>')

# 컨텐츠 리뷰 좋아요 api

# 컨텐츠 리뷰 댓글 관련 api

# 유저 로그인관련 api
api.add_resource(UserRegisterResource,"/register")
api.add_resource(UserLoginResource,"/login")
api.add_resource(UserLogoutResource,"/logout")
api.add_resource(UserIsEmail,"/isEmail")
api.add_resource(UserIsId,"/isId")
api.add_resource(UserIsNickname,"/isNickname")
api.add_resource(UserIspassword,"/ispassword")
api.add_resource(UserPasswordChanged,"/changedpassword")


# 유저 정보 관련 api
api.add_resource(UserContentLike,'/contentlike/me')

if __name__ == '__main__' : 
    app.run()

from flask import request
from flask_restful import Resource
from mysql.connector.errors import Error
from mysql_connection import get_connection
from flask_jwt_extended import jwt_required,get_jwt_identity

class search(Resource) :
    def post(self) :

        data = request.get_json()

        keyword = data["keyword"]
        genre = data["genre"]
        limit = data["limit"]
        rating = data["rating"]
        year = data["year"]
        offset = data["offset"]
        filtering = data["filtering"]
        sort = data["sort"]
        
        if filtering == "":
            filtering = "title"

        if filtering not in ["title","contentRating","createdYear"] :
            return {"sort_error":"필터 정렬 값 오류."}

        if sort == "":
            sort = "asc"

        if rating == "" : 
            rating = 0.0

        if year == "" :
            year = '1945-01-01'

        if genre == "" :
            genre = "[,]"

        if limit =="" :
            limit = "10"
        if offset =="":
            offset = "0"

        genre = genre.split(",")
        
        try :
            connection = get_connection()

            query='''select * 
                from content 
                where (title like "%'''+ keyword+'''%" or content like "%'''+ keyword+'''%" ) and type = "movie" and
                genre like "%'''+genre[0]+'''%" and genre like "%'''+genre[1]+'''%" and contentRating >= '''+str(rating)+''' and createdYear >= "'''+str(year)+'''"
                order by '''+filtering + ''' '''+sort+'''
                limit '''+ str(offset)+''',''' +str(limit)+''';'''
           
            
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query)

            movie_list = cursor.fetchall()
            i = 0 
            for row in movie_list :
                movie_list[i]['createdYear'] = row['createdYear'].isoformat()
                i = i + 1
            
            cursor.close()
            connection.close()

            query='''select * 
                from content 
                where (title like "%'''+ keyword+'''%" or content like "%'''+ keyword+'''%" ) and type = "tv" and
                genre like "%'''+genre[0]+'''%" and genre like "%'''+genre[1]+'''%" and contentRating >= '''+str(rating)+''' and createdYear >= "'''+str(year)+'''"
                order by '''+filtering + ''' '''+sort+'''
                limit '''+ str(offset)+''',''' +str(limit)+''';'''
            

            connection=get_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query)
            
            tv_list = cursor.fetchall()
            i = 0 
            for row in tv_list :
                tv_list[i]['createdYear'] = row['createdYear'].isoformat()
                i = i + 1

            cursor.close()
            connection.close()

            connection = get_connection()

            query = '''select * from actor where name like "%''' +keyword+'''%" ;  '''
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query)
            actor_list = cursor.fetchall()

            i = 0
            for row in actor_list :
                actor_list[i]['year'] = row['year'].isoformat()
                i = i + 1

            cursor.close()
            connection.close()     

        except Error as e :
            print(e)
            cursor.close()
            connection.close()
            return {"fail" : str(e)},500
        
        return {"movie" : movie_list,
                "tv":tv_list,
                "actor":actor_list},200

class contentLike(Resource) :
    @jwt_required()
    def post(self,contentId):
        userId = get_jwt_identity()

        try :
            connection = get_connection()

            query = '''insert into contentLike(contentId,contentLikeUserId)
                        values(%s,%s);'''
            record = (contentId,userId)

            cursor = connection.cursor()
            cursor.execute(query,record)

            connection.commit()


            cursor.close()

            connection.close()

        except Error as e :
            print(str(e))

            cursor.close()

            connection.close()

            return {'fail',str(e)},500
        
        return {"result":"success"},200

    @jwt_required()
    def delete(self,contentId) :
        userId = get_jwt_identity()

        try :
            connection = get_connection()

            query = '''delete from contentLike 
                    where contentId = %s and contentLikeUserId = %s ;'''
            
            record = (contentId, userId)

            cursor = connection.cursor()

            cursor.execute(query,record)

            connection.commit()

            cursor.close()

            connection.close()
        
        except Error as e : 
            print(str(e))

            cursor.close()

            connection.close()

            return {"error":str(e)},500

        return {"result":"success"},200
            
class contentReview(Resource) :
    @jwt_required()
    def post(self,contentId) :

        userId = get_jwt_identity()

        data = request.get_json()

        try:
            connection = get_connection()

            query = '''insert into contentReview(contentId,contentReviewUserId, title,content,userRating)
                        values(%s,%s,%s,%s,%s);'''
            
            record = (contentId,userId, data["title"],data["content"],data["userRating"])

            cursor = connection.cursor()

            cursor.execute(query,record)

            connection.commit()

            lastId = cursor.lastrowid

            cursor.close()

            connection.close()

        except Error as e :

            print(str(e))
            
            cursor.close()

            connection.close()

            return {"fail":str(e)},500

        return {"result":"success","contentReviewId":lastId},200

class contentReviewUD(Resource) :
    @jwt_required()
    def put(self ,contentId , contentReviewId) :
        
        userId = get_jwt_identity()
        
        data = request.get_json()
        
        try : 
            connection = get_connection()

            query = '''update contentReview 
                        set title = %s ,content = %s
                        where contentreviewId = %s and contentReviewUserId = %s
                        ;'''
            
            record = (data['title'],data['content'],contentReviewId,userId)

            cursor = connection.cursor()

            cursor.execute(query,record)

            connection.commit()

            cursor.close()

            connection.close()

        except Error as e :
            str(e)
            cursor.close()
            connection.close()

            return {'error':str(e)},500
        
        return {'result':'success'} , 200

    @jwt_required()
    def delete(self,contentId,contentReviewId) :
        userId = get_jwt_identity()
     
        try : 
            connection = get_connection()

            query = '''delete from contentReview
                    where contentReviewId = %s and contentReviewUserId = %s;
                        ;'''
            
            record = (contentReviewId,userId)

            cursor = connection.cursor()

            cursor.execute(query,record)

            connection.commit()

            cursor.close()

            connection.close()

        except Error as e :
            str(e)
            cursor.close()
            connection.close()

            return {'error':str(e)},500
        
        return {'result':'success'} , 200

class contentReviewLike(Resource) :
    @jwt_required()
    def post(self,contentReviewId) :
        userId = get_jwt_identity()

        try :
            connection = get_connection()

            query = '''insert into contentReviewLike(contentReviewId,contentReviewLikeUserId)
                        values(%s,%s);'''
            record = (contentReviewId , userId)

            cursor = connection.cursor()
            cursor.execute(query,record)

            connection.commit()

            cursor.close()
            connection.close()

        except Error as e :
            print(str(e))
            cursor.close()
            connection.close()
            return {"error":str(e)},500
        
        return {"result":"success"},200
    
    @jwt_required()
    def delete(self,contentReviewId) :
        userId = get_jwt_identity()

        try :
            connection = get_connection()

            query ='''delete from contentReviewLike 
                    where contentReviewId = %s and contentReviewLikeUserId = %s ;'''
            record = (contentReviewId , userId)

            cursor = connection.cursor()
            cursor.execute(query,record)

            connection.commit()

            cursor.close()
            connection.close()

        except Error as e :
            print(str(e))
            cursor.close()
            connection.close()
            return {"error":str(e)},500
        
        return {"result":"success"},200

class ReviewComment(Resource):
    @jwt_required()
    def post(self,contentReviewId) :
        userId = get_jwt_identity()
        data = request.get_json()
        try :
            connection = get_connection()

            query = '''insert into contentReviewComment(contentReviewId , commentUserId , comment )
                        values (%s,%s,%s);'''
            record = (contentReviewId,userId,data['comment'])

            cursor = connection.cursor()

            cursor.execute(query,record)

            connection.commit()

            lastId = cursor.lastrowid
            cursor.close()

            connection.close()
        except Error as e :
            print(str(e))
            cursor.close()
            connection.close()
            return {'error':str(e)},500
        
        return {'result':'success','commentId':lastId},200

class ReviewCommentUD(Resource):
    @jwt_required()
    def delete(self,contentReviewId,commentId) :
        
        userId = get_jwt_identity()

        try : 
            connection = get_connection()

            query = '''delete from contentReviewComment
                    where commentId = %s and contentReviewId = %s and commentUserId = %s ;'''
            record = (commentId,contentReviewId,userId)

            cursor = connection.cursor()

            cursor.execute(query,record)

            connection.commit()

            cursor.close()

            connection.close()

        except Error as e :
            print(str(e))

            cursor.close()

            connection.close()

            return {'error':str(e)},500
        return {'result':'success'},200        

    @jwt_required()
    def put(self,contentReviewId,commentId) :

        userId = get_jwt_identity()

        data = request.get_json()

        try :
            connection = get_connection()

            query = '''update contentReviewComment
                        set comment = %s
                        where commentId = %s and contentReviewId = %s and commentUserId = %s;'''
            record = (data['comment'],commentId,contentReviewId,userId)

            cursor = connection.cursor()

            cursor.execute(query,record)

            connection.commit()

            cursor.close()

            connection.close()

        except Error as e :
            print(str(e))

            cursor.close()

            connection.close()

            return {'error':str(e)},500

        return {'result':'success'},200        


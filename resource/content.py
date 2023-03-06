from flask import request
from flask_restful import Resource
from mysql.connector.errors import Error
from mysql_connection import get_connection
from flask_jwt_extended import jwt_required,get_jwt_identity

class search(Resource) :
    def get(self) :

        keyword = request.args.get("keyword")
        genre = request.args.get("genre")
        limit = request.args.get("limit")
        rating = request.args.get("rating")
        year = request.args.get("year")
        offset = request.args.get("offset")
        if rating == "" : 
            rating = 5.0

        if year == "" :
            year = '2020-01-01'

        genre = genre.split(",")
        print(year)
        try :
            connection = get_connection()

            query='''select * 
                from content 
                where title like "% '''+ keyword+'''%" and type = "movie" and
                genre like "%'''+genre[0]+'''%" and genre like "%'''+genre[1]+'''%" and contentRating >= '''+str(rating)+''' and createdyear >= "'''+str(year)+'''"
                limit '''+offset+''',''' +limit+''';'''
           
            
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query)

            movie_list = cursor.fetchall()

            i = 0 
            for row in movie_list :
                movie_list[i]['createdYear'] = row['createdYear'].isoformat()
                i = i + 1

            query = '''select * 
                    from content 
                    where title like "%'''+keyword+'''%" and type = "tv" and
                    genre like "%'''+genre[0] + '''%" and genre like "%'''+genre[1] +'''%"
                    limit 10 ,'''  + limit + '''; '''
            
            cursor.execute(query)

            tv_list = cursor.fetchall()
            i = 0 
            for row in tv_list :
                tv_list[i]['createdYear'] = row['createdYear'].isoformat()
                i = i + 1

            cursor.close()
            connection.close()

        except Error as e :
            print(e)
            cursor.close()
            connection.close()
            return {"fail" : str(e)},500
        
        return {"movie" : movie_list,
                "drama" : tv_list},200



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

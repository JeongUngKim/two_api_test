from flask import request
from flask_restful import Resource
from mysql.connector import Error
from flask_jwt_extended import create_access_token, get_jwt, jwt_required
from mysql_connection import get_connection
from email_validator import validate_email, EmailNotValidError
from utils import check_password, hash_password

class UserRegisterResource(Resource) :
    def post(self) :
#         {
#           "nickname" : "성태",
#            "userEmail" : "abc123@naver.com",
#            "password" : "1234",
#            "gender" : "1",
#            "age" :"28"
#           }

         # 1. 클라이언트가 보낸 데이터를 받아준다.
        data = request.get_json()
        # 2. 이메일 주소형식이 올바른지 확인한다. 
        try : 
            validate_email( data["userEmail"] )
        except EmailNotValidError as e :
            print(str(e))
            return {'error' : str(e)} , 400
        
        # 3. 비밀번호의 길이가 유효한지 체크한다.
        # 만약, 비번이 4자리 이상, 12자리 이하다라면,

        if len( data['password'] ) < 4 or len( data['password'] ) > 12 :
            return {'error' : '비밀번호 길이 확인'} , 400
        
         # 4. 비밀번호를 암호화 한다.
        hashed_password = hash_password( data['password']  )

        # 5. DB 에 회원정보를 저장한다.
        try:
            connection = get_connection()
            query = '''insert into user(nickname,userEmail,password,gender,age)
                        values(%s,%s,%s,%s,%s);'''
            record = ( data["nickname"], data["userEmail"],hashed_password ,
                      data["gender"],data["age"] )
            cursor = connection.cursor()
            cursor.execute(query,record)
            connection.commit()

            userId = cursor.lastrowid

            cursor.close()
            connection.close()
        except Error as e :
            print(e)
            cursor.close()
            connection.close()
            return {'error' : str(e)}, 500
        
        access_token = create_access_token(userId)
        return {'result' : 'success', 'access_token' : access_token}, 200
    
class UserLoginResource(Resource) :
    def post(self) :
#         {
#     "userEmail":"abc@naver.com",
#     "password" : "1234"}

        data = request.get_json()
        print(data)
        
         # 2. DB 로부터 해당 유저의 데이터를 가져온다.
        try :
            #커넥션은 연결해주는거
            connection = get_connection()
            query ='''select* 
                    from user
                    where userEmail= %s;'''
            record = ( data['userEmail'] ,  )

            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, record)
            #바로 보여지는 에러 확인
            print('쿼리 실행 ' + query)
            print(record)
            #select를 사용할때는 fetchall을 사용한다
            result_list = cursor.fetchall()
            print(result_list)
           # 저장되것이 없으면 0이면 리턴이 클라이언트에 보여준다
            if len(result_list) == 0 :
                return {'error' : '회원가입한 사람 아닙니다.'}, 400
            # 수많은 리스트중 하나씩 가져와서 반복문 돌릴수없으니 index를 0으로하고 +1더하는 형식으로 코드를 완성합니다
            index = 0
            for colrow in result_list :
                result_list[index]['createdAt'] = colrow['createdAt'].isoformat()
                index = index + 1 

            print(result_list[0]['createdAt'])
            cursor.close()
            connection.close()
        except Error as e:
            print(e)
            cursor.close()
            connection.close()
            return {"error" : str(e)}, 500
         
         # 비밀번호가 일치하지 않을때 코드
        check = check_password( data['password'], result_list[0]['password'] )

        if check == False :
            return {"error" : "비밀번호가 일치하지 않습니다"} , 400

        access_token = create_access_token( result_list[0]['id'] )

        return {"result" : "success", "access_token" : access_token}, 200
    
jwt_blacklist = set()

class UserLogoutResource(Resource) :
    @jwt_required()
    def post(self) :
        
        jti = get_jwt()['jti']
        print(jti)

        jwt_blacklist.add(jti)

        return {'result' : 'success'}, 200
    
class UserIspassword(Resource):
    def post(self) :
        # {
        #     "userEmail" : "abc123@naver.com"
        # }

        # 1. 클라이언트 로부터 데이터를 받아온다.
        data = request.get_json()

        # 2. 받아온 데이터를 통해 서버 쿼리문을 실행한다.
        try : 
            connection = get_connection()
            query = '''select *
                    from user
                    where userEmail = %s ;'''
            record = ( data["userEmail"] , )

            cursor = connection.cursor(dictionary=True)

            cursor.execute(query,record)

            result_list = cursor.fetchall()

            if len(result_list) == 0 :
                return {"error" : "회원이 아닙니다."},400
            
            cursor.close()
            connection.close()

        except Error as e :
            cursor.close()
            connection.close()

        return {"result":"success","userEmail":result_list[0]["userEmail"]},200

class UserPasswordChanged(Resource):
    def post(self) :
        # { userEmail : abc@naver.com 
        #   newpassword : 1234 }

        data = request.get_json()

        password = hash_password(data["newpassword"])
        try :
            connection = get_connection()

            query = '''update user
                        set password = %s
                        where userEmail = %s;'''
            record = (password , data["userEmail"])

            cursor = connection.cursor()
            cursor.execute(query,record)

            connection.commit()

            cursor.close()
            connection.close()
        except Error as e :
            cursor.close()
            connection.close()

        return {"result":"success"},200
 
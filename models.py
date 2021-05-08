from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy() #SQLAlchemy를 사용해 데이터베이스 저장

class User(db.Model): #데이터 모델을 나타내는 객체 선언
    __tablename__ = 'user_table' #테이블 이름 : user_table
    
    id = db.Column(db.Integer, primary_key=True)    #id를 프라이머리키로 설정
    email = db.Column(db.String(32), unique=True, nullable=False)   #패스워드를 받아올 문자열길이
    userid = db.Column(db.String(32), unique=True, nullable=False)  #이하 위와 동일
    password = db.Column(db.String(8), nullable=False)

    def __init__(self, email, password):
        self.email = email
        self.set_password(password)
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
 
    def check_password(self, password):
        return check_password_hash(self.password, password)

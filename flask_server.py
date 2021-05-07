import json, os
from flask import Flask, render_template, request, redirect, session, escape, jsonify
from flask_sqlalchemy import SQLAlchemy
from Models import db, User
from werkzeug.utils import secure_filename
import classifier, similar, rnn_lstm
import connect_db

# HTTP 서버 실행하기
UPLOAD_FOLDER = './uploads'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

color_list = ['베이지색', '검정색', '갈색', '회색', '초록색', '파란색', '빨간색', '하얀색']
cloth_list = ['긴팔티셔츠', '셔츠', '맨투맨_후드', '면바지', '반바지', '반팔', '블라우스', 
 '스커트', '원피스', '청바지', '카디건', '트레이닝복']
 
# web 렌더링
@app.route("/", methods=['GET'])
def index() :
  return render_template('index.html')

@app.route("/upload", methods=['GET','POST'])
def upload() :
  return render_template('upload.html')

@app.route("/register", methods=['GET', 'POST'])  #GET(정보보기), POST(정보수정) 메서드 허용
def register() :
  return render_template('register.html')

@app.route("/login", methods=['GET'])
def login() :
  return render_template('login.html')

@app.route("/detail", methods=['GET'])
def detail() :
  return render_template('detail.html')


# app 부분
@app.route('/cnn_process', methods=['GET','POST'])
def cnn_process():
  # file과 file 이름 가져오기
  f = request.files['file']
  # print(f)
  filename = secure_filename(f.filename)

  # CNN으로 옷 종류, 색깔 판별
  # json은 numpy type 못받으므로 int로 형변환
  cloth = int(classifier.get_cloth(f))
  color = int(classifier.get_color(f))

  # 옷 종류와 색깔 json으로 dump
  return json.dumps({
    "cloth": cloth,
    "color": color
  })

@app.route('/cosine_process', methods=['GET','POST'])
def cosine_process():
  # file 가져오기
  f2 = request.files['file']

  # Json으로 Post받은 카테고리 가져오고 int로 변환
  category = int(request.form.get("category"))

  # cosine 유사도로 비슷한 이미지의 가격정보 가져오기
  result = similar.get_similar(f2, category)
  # print(category)
  # print(result)

  # 최대, 최소, 평균 가격 json으로 dump
  return json.dumps({
    "max": result[0],
    "min": result[1],
    "mean": result[2],
    "img1": result[3][0],
    "img2": result[3][1],
    "img3": result[3][2]
  })

@app.route('/rnn_process', methods=['GET','POST'])
def rnn_process():

  # Json으로 Post받은 카테고리 가져오고 int로 변환
  data = request.get_json()
  category = int(data['category'])

  # category를 문자로 바꿈
  category = cloth_list[category]
  print(category)

  # 카테고리를 시드로 문장 생성
  result = rnn_lstm.generate_text(category)
  print(result)
  
  # 생성한 문장 json으로 dump
  return json.dumps({
  "text": result
  })

@app.route('/upload_process', methods=['GET','POST'])
def upload_process():
  f3 = request.files['file']
  filename = secure_filename(f3.filename)
  q = request.form
  user = 1

  connect_db.upload(q['title'],int(q['price']),q['contents'],q['deliver'],
                  q['status'],color_list[int(q['color'])],q['washing'],q['size'],user,int(q['category']))

  print(f3)
  print(q)
  
  # 업로드 ( .save(경로) )
  f3.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
  return render_template('upload_complete.html')

# 서버 구동
if __name__ == '__main__':
  # 데이터베이스
  basedir = os.path.abspath(os.path.dirname(__file__)) #현재 파일이 있는 디렉토리 절대 경로
  dbfile = os.path.join(basedir, 'db.sqlite') #데이터베이스 파일을 만든다

  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile
  app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True #사용자에게 정보 전달완료하면 teadown. 그 때마다 커밋=DB반영
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #추가 메모리를 사용하므로 꺼둔다

  # db = SQLAlchemy() #SQLAlchemy를 사용해 데이터베이스 저장
  db.init_app(app) #app설정값 초기화
  db.app = app #Models.py에서 db를 가져와서 db.app에 app을 명시적으로 넣는다
  db.create_all() #DB생성

  app.run(host="127.0.0.1", port="5000", debug=True)


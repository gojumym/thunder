import pymysql

def connect_db(database):
    # DB 호스트 정보에 맞게 입력해주세요
    db = None
    db = pymysql.connect(
        host='127.0.0.1',
        user='root',
        passwd='password123',
        db=database,
        charset='utf8',
        port=3306
    )
    return db

def register(email, passwd, name, town, phone, gender):
    db = None
    try:
        db = connect_db('thunder')
        # 데이터 삽입 sql 정의
        with db.cursor() as cursor:
            sql = '''
                    INSERT INTO user(user_email, user_passwd, user_name, user_town, user_phone, user_gender) values("%s", "%s", "%s", "%s", "%s", "%s")
                    ''' % (email, passwd, name, town, phone, gender)
            cursor.execute(sql)
        db.commit() # 커밋

    except Exception as e:
        print(e)

    finally:
        if db is not None:
            db.close()

def upload(title,price,contents,deliver,status,color,washing,size,user_uid,category_id):
    db = None
    try:
        db = connect_db('thunder')

        # 데이터 삽입 sql 정의
        with db.cursor() as cursor:
            sql = '''
                    INSERT INTO product(pd_title, pd_price, pd_contents, pd_deliver, pd_status, pd_color, pd_washing, pd_size, user_uid, category_id) values("%s", %d, "%s", "%s", "%s", "%s", "%s", "%s", %d, %d)
                    ''' % (title, price, contents, deliver, status, color, washing, size, user_uid, category_id)
            cursor.execute(sql)
        db.commit() # 커밋

    except Exception as e:
        print(e)

    finally:
        if db is not None:
            db.close()

if __name__ == '__main__':
    # module test code
    # register('zebok@naver.com', 'password123', '이준호', '서울시 종로구', '010-5125-8988', 'M')
    upload("끼에엑",1000,"후드티 쓰레기","착불","중고","하얀색","손세탁","M",1,2)

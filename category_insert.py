import connect_db

cloth_list = ['긴팔티셔츠', '셔츠', '맨투맨_후드', '면바지', '반바지', '반팔', '블라우스', 
 '스커트', '원피스', '청바지', '카디건', '트레이닝복']

def category_insert(cat_id,cat_name):
    db = None
    try:
        db = connect_db.connect_db('thunder')

        # 데이터 삽입 sql 정의
        with db.cursor() as cursor:
            sql = '''
                    insert INTO category values("%d","%s")
                    ''' % (cat_id, cat_name)
            cursor.execute(sql)
        db.commit() # 커밋

    except Exception as e:
        print(e)

    finally:
        if db is not None:
            db.close()

if __name__ == '__main__':
    i = 0
    for cat in cloth_list:
        category_insert(i,cat)
        i += 1



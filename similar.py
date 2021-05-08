import os
import pandas as pd
import cv2
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import platform

# dataset의 종류 리스트
cloth_list = ['긴팔티셔츠', '셔츠', '맨투맨_후드', '면바지', '반바지', '반팔', '블라우스', 
              '스커트', '원피스', '청바지', '카디건', '트레이닝복']

def search(dirname):
    search_list = []
    filenames = os.listdir(dirname)
    for filename in filenames:
        full_filename = os.path.join(dirname, filename)
        search_list.append(full_filename)
    return search_list

def get_similar(image, category):
    # directory 설정
    if platform.system()=='Windows':
        root_dir = '.\\data'
    else:
        root_dir = './data'

    # # category 1 빼주기(1에서 시작하지만 list는 0부터 시작)
    # category = category - 1

    # 이미지 resize
    # img = cv2.imread(image)

    # img = cv2.resize(img, (64,64))
    # img_np = np.array(img)
    # img_np = img_np/255
    # img_np = img_np.reshape(1,-1)
    # print("cv2로 했을 때")
    # print(img_np.shape)

    img = Image.open(image)
    img = img.convert("RGB")
    img = img.resize((64,64))
    data = np.asarray(img)

    img_np = np.array(data)
    img_np = img_np.astype("float") / 255
    img_np = img_np.reshape(1, -1)

    # print("PIL로 했을 때")
    # print(img_np.shape)

    result = []
    # category로 읽어와야 함

    meta_dir = search(os.path.join(root_dir, 'meta'))
    npy_dir = search(os.path.join(root_dir, 'npy'))
    pickle_dir = search(os.path.join(root_dir, 'pickle'))
    img_dir = search(os.path.join('.\\static', 'img'))

    # npy, list 읽어오기
    img_list = np.load(npy_dir[category])

    with open(pickle_dir[category], 'rb') as f:
        img_path_list = pickle.load(f)
    # meta-data 불러오기
    meta = pd.read_csv(meta_dir[category], encoding='utf-8')

    # cosine 비교
    for i in range(len(img_list)):
        similarity_simple_pair = cosine_similarity(img_np, img_list[i])
        result.append(similarity_simple_pair)

    # list_df의 img_id 데이터 경로에서 숫자값만 추출
    img_id_list = []
    img_id_ub_list = []

    for i in range(len(img_path_list)):
        k = os.path.basename(img_path_list[i])
        k = os.path.splitext(k)
        img_id_list.append(int(k[0].split('_')[0]))
        img_id_ub_list.append(int(k[0].split('_')[1]))

    # 데이터 프레임 생성
    data = pd.DataFrame({'img_id':img_id_list, 'img_id_ub':img_id_ub_list, 'num':result})
    data = data.sort_values(by='num', ascending=False)
    data = data.reset_index(drop=True)
    data = data.drop_duplicates('img_id', keep = 'first')
    data.reset_index(drop=True, inplace=True)


    test2 = pd.merge(data, meta, on='img_id')
    test3 = test2[['img_id', 'img_id_ub', 'num', 'price']][:10]

    # 데이터 정제
    test3['price'] = test3['price'].str.replace('원',' ')
    test3['price'] = test3['price'].replace({',': ''}, regex=True)
    test3['price'] = pd.to_numeric(test3['price'])

    print(test3.head(5))

    # 유사도 높은 상위 10개 상품의 가격을 매기기
    p_mean = int(test3['price'].mean())
    p_max = int(test3['price'].max())
    p_min = int(test3['price'].min())
    p_img_id = []
    
    
    for i in range(len(test3)):
        img_id = str(test3['img_id'][i]) + "_" + str(test3['img_id_ub'][i]) + ".jpg"
        img_path = os.path.join(img_dir[category], img_id)
        p_img_id.append(img_path)

    result = [p_max, p_min, p_mean, p_img_id]

    return result

if __name__ == '__main__':
    # module test code
    my_cloth = get_similar('./test_data/test.jpg', 4)
    print('최대가 : {}원'.format(my_cloth[0]))
    print('최소가 : {}원'.format(my_cloth[1]))
    print('평균가 : {}원'.format(my_cloth[2]))
    print(my_cloth[3][0])

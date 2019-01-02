# coding: utf-8
import os, sys
import cv2
import math
import numpy as np

IMAGE_FOLDER = 'app/assets/images'
UPLOAD_FOLDER = 'public/images/tmp'

def apply_filter(img_stream):
    # データ形式の変換
    img_array = np.asarray(bytearray(img_stream.read()), dtype=np.uint8)
    img = cv2.imdecode(img_array, 1)

    # スクリーントーン画像の読み込み
    SCREEN_FILENAME = 'screen_2_600.jpg'
    screen_path = os.path.join(IMAGE_FOLDER, SCREEN_FILENAME)
    screen = cv2.imread(screen_path)

    # 画像の漫画化
    filtered_img = comic_filter(img, screen, 60, 150)

    # 画像の一時保存
    id = str(count_files(UPLOAD_FOLDER))
    str_list = [id,'jpg']
    tmp_name = '.'.join(str_list)
    tmp_path = os.path.join(UPLOAD_FOLDER, tmp_name)
    cv2.imwrite(tmp_path, filtered_img)

    # 結果を出力
    f = open(tmp_path, 'rb')
    output_img = f.read()
    return output_img

# 漫画化フィルタ
def comic_filter(src, screen, th1=60, th2=150):

    # 画像をリサイズ
    src = resize_img(src, 600)

    # 正方形にトリミング
    src = clip_to_square(src)

    # グレースケール変換
    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

    # Cannyアルゴリズムで輪郭検出し、色反転
    edge = 255 - cv2.Canny(gray, 80, 120)

    # 三値化
    gray[gray <= th1] = 0
    gray[gray >= th2] = 255
    gray[ np.where((gray > th1) & (gray < th2)) ] = screen[ np.where((gray > th1)&(gray < th2)) ]

    # 三値画像と輪郭画像を合成
    return cv2.bitwise_and(gray, edge)

def count_files(target_dir_name):
    #カウンタの初期化
    cnt = 0
    # 指定したパス内の全てのファイルとディレクトリを要素とするリストを返す
    target_dir_files = os.listdir(target_dir_name)
    for file in target_dir_files:
        new_target_dir_name = target_dir_name + "\\" +file
        #ディレクトリか非ディレクトリで条件分岐
        if os.path.isdir(new_target_dir_name):
            #ディレクトリの場合、中に入って探索する
            cnt += countFiles(new_target_dir_name)
        else:
            #非ディレクトリの場合、数え上げを行う
            cnt += 1
    return cnt

def resize_img(img, size):
    height = img.shape[0]
    width = img.shape[1]
    if height > width:
        height = int(size / width * height)
        width = size
    else:
        width = int(size / height * width)
        height = size
    return cv2.resize(img,(width, height))

def clip_to_square(img):
    height = img.shape[0]
    width = img.shape[1]
    if height > width:
        y0 = int((height - width) / 2)
        y1 = y0 + width
        img = img[y0:y1, 0:width]
    else:
        x0 = int((width - height) / 2)
        x1 = x0 + height
        img = img[0:height, x0:x1]
    return img

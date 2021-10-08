from PIL import Image
import numpy as np
import sqlite3
import os
import io
import cv2

SIZE = 64, 64

train_path = 'static/images/train'
test_path  = 'static/images/test'

class_names = ('joy', 'fear', 'anger', 'surprise', 'sadness')


def rgb2gray(img_obj):
    #ret = img_obj
    #if not is_grayscale(img_obj):
    #ret = img_obj.convert('L')
    gray = cv2.cvtColor(img_obj, cv2.COLOR_BGR2GRAY)
    return gray

def is_grayscale(img_obj):
    img = img_obj.convert('RGB')
    w, h = img.size
    for i in range(w):
        for j in range(h):
            r, g, b = img.getpixel((i,j))
            if r != g != b: 
                return False
    return True

def resize_img(img_obj):
    res = img_obj
    if not check_size(img_obj):
        res = cv2.resize(img_obj, dsize=SIZE, interpolation=cv2.INTER_CUBIC)
    return res

def check_size(img):
    width, height = img.shape
    if (width,height) == SIZE:
        return True
    else: return False 

def check_img(img_path):
    img = cv2.imread(img_path)

    img = rgb2gray(img)

    img = resize_img(img)
    #img.close()
    return img

def create(path, dbname='autisso.db'):
    connection = sqlite3.connect(dbname)

    with open('schema.sql') as f:
        connection.executescript(f.read())

    cur = connection.cursor()

    for i in class_names:
        cur.execute("INSERT INTO labels (name) VALUES (?)", (i,))

    for i,v in enumerate(class_names):
        res = os.listdir(os.path.join(path, v))
        for j in res:
            p = os.path.join(path, v, j)
            img_obj = check_img(p)
            buf = io.BytesIO()
            is_success, buffer = cv2.imencode(".png", img_obj)
            buf = io.BytesIO(buffer)
            b = buf.getvalue()
            cur.execute("INSERT INTO images (label_id, img) VALUES (?, ?)", (i+1, b))
        
    connection.commit()
    connection.close()

if __name__ == '__main__':
    create(train_path,'train.db')
    create(test_path, 'test.db')
from PIL import Image
import sqlite3
import os
import io

SIZE = 64

rel_path = 'static/images'

LABELS = ('joy', 'fear', 'anger', 'surprise', 'sadness')


def rgb2gray(img_obj):
    ret = img_obj
    #if not is_grayscale(img_obj):
    ret = img_obj.convert('LA')
    return ret

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
    ret = img_obj
    if not check_size(img_obj):
        img_obj.thumbnail((SIZE,SIZE) , Image.ANTIALIAS)
    return ret

def check_size(img):
    width, height = img.size
    if width == SIZE and height == SIZE:
        return True
    else: return False 

def check_img(img_path):
    img = Image.open(img_path)

    img = rgb2gray(img)

    img = resize_img(img)
    #img.close()
    return img

connection = sqlite3.connect('autisso.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

for i in LABELS:
    cur.execute("INSERT INTO labels (name) VALUES (?)", (i,))

for i,v in enumerate(LABELS):
    res = os.listdir(os.path.join(rel_path, v))
    for j in res:
        p = os.path.join(rel_path, v, j)
        img_obj = check_img(p)
        buf = io.BytesIO()
        img_obj.save(buf, format='PNG')
        b = buf.getvalue()
        cur.execute("INSERT INTO images (label_id, img) VALUES (?, ?)", (i+1, b))
        
connection.commit()
connection.close()
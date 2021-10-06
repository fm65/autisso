from itertools import groupby
import sqlite3
import matplotlib.pyplot as plt
import matplotlib.image as img
import tempfile


def show_img(data, title=''):
    filename = tempfile.NamedTemporaryFile()
    filename.file.write(data)
    image = img.imread(filename)
    plt.title(title)
    plt.imshow(image)
    plt.show()

def get_db_connection():
    conn = sqlite3.connect('autisso.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_img_from_db(debug=False):
    conn = get_db_connection()
    data = conn.execute('SELECT i.img, l.name FROM images i JOIN labels l \
                        ON i.label_id = l.id ORDER BY l.name;').fetchall()

    result = {}

    for k, g in groupby(data, key=lambda t: t['name']):
        result[k] = list(g)

    if debug:
        for k,v in result.items(): #DEBUG
            for i in v:
                show_img(i[0], k)
    
    conn.close()

    return result

get_img_from_db(debug=True)
from itertools import groupby
import sqlite3
import matplotlib.pyplot as plt
import matplotlib.image as img
import tempfile


def show_img_from_db(data, title=''):
    filename = tempfile.NamedTemporaryFile()
    filename.file.write(data)
    image = img.imread(filename)
    plt.title(title)
    plt.imshow(image)
    plt.show()

def get_db_connection(dbname='autisso.db'):
    conn = sqlite3.connect(dbname)
    conn.row_factory = sqlite3.Row
    return conn

def get_img_from_db(dbname='autisso.db', debug=False):
    conn = get_db_connection(dbname)
    data = conn.execute('SELECT i.img, l.name FROM images i JOIN labels l \
                        ON i.label_id = l.id ORDER BY l.name;').fetchall()

    result = {}

    for k, g in groupby(data, key=lambda t: t['name']):
        result[k] = [x[0] for x in list(g)]

    if debug:
        for k,v in result.items(): #DEBUG
            for i in v:
                show_img_from_db(i, k)
    
    conn.close()

    return result

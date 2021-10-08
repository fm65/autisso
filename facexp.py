from collections import OrderedDict
from PIL import Image
import numpy as np
import random
import io
import db

path = 'datasets/facexp.npz'

class_names = ('joy', 'fear', 'anger', 'surprise', 'sadness')

to_np_array = lambda img_bytes: np.array(Image.open(io.BytesIO(img_bytes)))

def create_data(dbname='train.db'):
    img_dict = db.get_img_from_db(dbname)
    
    sorted_dict = OrderedDict([(i, img_dict[i]) for i in class_names])
    x,y = [], []
    for i,values in enumerate(sorted_dict.values()):
        for v in values:
            x.append(to_np_array(v))
            y.append(i)
    
    # Shuffle x,y at once with same order
    c = list(zip(x, y))
    random.shuffle(c)
    x, y = zip(*c)
    
    return x,y

def save(path, x_train, y_train, x_test, y_test):
    np.savez(path, x_train=x_train, y_train=y_train, 
                   x_test=x_test,  y_test=y_test)

def load_data():
    """Loads the FACEXP dataset.
    This is a dataset of 100 64x64 grayscale images of the 5 facial expression,
    along with a test set of 50 images.
    Returns:
        Tuple of NumPy arrays: `(x_train, y_train), (x_test, y_test)`.
    **x_train**: uint8 NumPy array of grayscale image data with shapes
        `(100, 64, 64)`, containing the training data. Pixel values range
        from 0 to 255.
    **y_train**: uint8 NumPy array of facial expression labels (integers in range 0-4)
        with shape `(100,)` for the training data.
    **x_test**: uint8 NumPy array of grayscale image data with shapes
        (50, 64, 64), containing the test data. Pixel values range
        from 0 to 255.
    **y_test**: uint8 NumPy array of facial expression labels (integers in range 0-4)
        with shape `(50,)` for the test data.
    Example:
    ```python
    (x_train, y_train), (x_test, y_test) = dataset.load_data()
    assert x_train.shape == (100, 64, 64)
    assert x_test.shape == (50, 64, 64)
    assert y_train.shape == (100,)
    assert y_test.shape == (50,)
    ```
    """
    with np.load(path, allow_pickle=True) as f:
        x_train, y_train = f['x_train'], f['y_train']
        x_test, y_test = f['x_test'], f['y_test']

        return (x_train, y_train), (x_test, y_test)

if __name__ == '__main__':
    x_train, y_train = create_data('train.db')
    x_test, y_test  = create_data('test.db')
    save(path, x_train, y_train, x_test, y_test)
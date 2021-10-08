"""
Level | Level for Humans | Level Description                  
 -------|------------------|------------------------------------ 
  0     | DEBUG            | [Default] Print all messages       
  1     | INFO             | Filter out INFO messages           
  2     | WARNING          | Filter out INFO & WARNING messages 
  3     | ERROR            | Filter out all messages 
"""     
import os, sys
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # or any {'0', '1', '2'}
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

import facexp
from init_db import check_img

class_names = ('joy', 'fear', 'anger', 'surprise', 'sadness')

(train_images, train_labels), (test_images, test_labels) = facexp.load_data()

input_shape=(64, 64)

train_images = train_images / 255.0

test_images = test_images / 255.0

model = tf.keras.Sequential([
    tf.keras.layers.Flatten(input_shape=input_shape),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(5)
])

def train(epochs=10):
    model.compile(optimizer='adam',
                loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                metrics=['accuracy'])

    model.fit(train_images, train_labels, epochs=epochs)

    test_loss, test_acc = model.evaluate(test_images,  test_labels, verbose=2)
    
    return test_loss, test_acc

def predict(image):
    probability_model = tf.keras.Sequential([model, 
                                            tf.keras.layers.Softmax()])

    predictions = probability_model.predict(image)
    
    return predictions

def plot_image(i, predictions_array, true_label, img):
    true_label, img = true_label[i], img[i]
    plt.grid(False)
    plt.xticks([])
    plt.yticks([])

    plt.imshow(img, cmap=plt.cm.binary)

    predicted_label = np.argmax(predictions_array)
    if predicted_label == true_label:
        color = 'blue'
    else:
        color = 'red'

    plt.xlabel("{} {:2.0f}% ({})".format(class_names[predicted_label],
                                    100*np.max(predictions_array),
                                    class_names[true_label]),
                                    color=color)

def plot_value_array(i, predictions_array, true_label):
    true_label = true_label[i]
    plt.grid(False)
    plt.xticks(range(5))
    plt.yticks([])
    thisplot = plt.bar(range(5), predictions_array, color="#777777")
    plt.ylim([0, 1])
    predicted_label = np.argmax(predictions_array)

    thisplot[predicted_label].set_color('red')
    thisplot[true_label].set_color('blue')

def classify(i, predictions_array, true_label, training=True):
    if training: train()
    true_label = true_label[i]
    predicted_label = np.argmax(predictions_array)
    probability = predictions_array[predicted_label]

    true_label = class_names[true_label]
    predicted_label = class_names[predicted_label]
    probability = int(probability*100)

    return true_label, predicted_label, probability

def classify_one(image, training=False):
    h,w = image.shape
    x = image.reshape(1, h, w)
    predictions = predict(x)
    res = classify(0, predictions[0], test_labels, training=training)
    if not training:
        res = res[1:]
    return res

def debug():
    # Plot the first X test images, their predicted labels, and the true labels.
    # Color correct predictions in blue and incorrect predictions in red.
    num_rows = 5
    num_cols = 4
    num_images = num_rows*num_cols
    predictions = predict()
    plt.figure(figsize=(2*2*num_cols, 2*num_rows))
    for i in range(num_images):
        plt.subplot(num_rows, 2*num_cols, 2*i+1)
        plot_image(i, predictions[i], test_labels, test_images)
        plt.subplot(num_rows, 2*num_cols, 2*i+2)
        plot_value_array(i, predictions[i], test_labels)
    plt.tight_layout()
    plt.show()


#print("true_label:", "predicted_label:", "probability:")
#predictions = predict(test_images)
#for i in range(20):
#    res = classify(i, predictions[i], test_labels)
#    print(res[0], res[1], res[2])

#img = check_img('test.png')
#res = classify_one(img)
#print(res)
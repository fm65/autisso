from flask import Flask, Response, request, render_template, redirect, url_for
from image import *
from classifier import classify_one
from init_db import check_img
import os

class_names = ('joy', 'fear', 'anger', 'surprise', 'sadness')

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    predicted_label = ''
    probability = 0
    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            filename = uploaded_file.filename
            uploaded_file.save(filename)
            _, file_extension = os.path.splitext(filename)
            new_filename = 'test'+file_extension
            os.rename(filename, new_filename)
        img = check_img(new_filename)
        res = classify_one(img)
        predicted_label = res[0]
        probability = res[1]
        return redirect(url_for('index', predicted_label=predicted_label, 
                                         probability=probability, class_names=class_names))
    return render_template('index.html', 
           predicted_label=predicted_label, probability=probability, class_names=class_names)

@app.route('/webcam', methods=['GET', 'POST'])
def webcam():
    global video
    return Response(from_webcam(video),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/game')
def game():
    return render_template ('game.html')

if __name__ == '__main__':
    app.run(threaded=True)


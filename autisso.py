from flask import Flask, Response, request, render_template
from image import *

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/image', methods=['GET', 'POST'])
def image():
    filename = request.args.get('filename', default='static/test.png', type=str)
    return f"<h1> From Image: {filename} </h1>"

@app.route('/webcam', methods=['GET', 'POST'])
def webcam():
    global video
    return Response(from_webcam(video),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(threaded=True)
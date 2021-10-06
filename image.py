import cv2

face_cascade = cv2.CascadeClassifier()
face_cascade.load(cv2.samples.findFile("static/haarcascade_frontalface_alt.xml"))

def from_image(filename=None):
    img = cv2.imread(filename)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
    cv2.imshow('img', img)
    cv2.waitKey()


video = cv2.VideoCapture(0)

def from_webcam(video, filename=None):
    if filename is not None:
        # To use a video file as input 
        video = cv2.VideoCapture(filename)

    while True:
        is_success, img = video.read()
        gray  = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray  = cv2.equalizeHist(gray)
        faces = face_cascade.detectMultiScale(gray)

        for (x, y, w, h) in faces:
            center = (x + w//2, y + h//2)
            cv2.putText(img, "X: " + str(center[0]) + " Y: " + 
                str(center[1]), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
            img = cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
        ret, png = cv2.imencode('.png', img)

        k = cv2.waitKey(30) & 0xff
        if k == 27: break #TODO

        frame = png.tobytes()    
        
        yield (b'--frame\r\n'
               b'Content-Type: image/png\r\n\r\n' + frame + b'\r\n\r\n')
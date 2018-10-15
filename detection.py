import os

from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
# import imutils

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText

def sendMailWithImage(fromEmail, password, toEmail, body, subject, filename):
    file = open(filename, "rb")
    msg = MIMEMultipart()
    msg['From'] = fromEmail
    msg['To'] = toEmail
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    msg.attach(MIMEImage(file.read()))
   
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromEmail, password)
    server.sendmail(fromEmail, toEmail, msg.as_string())
    server.quit()
    file.close()

def processImageFromCamera(frame):
    image = frame.array
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags = cv2.CASCADE_SCALE_IMAGE)

    if len(faces) > 0:
        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 100), 1)
        cv2.imwrite('detected.png',image)
        sendMailWithImage('your from email', 'your from email password', 'your to email', 'Intruder detected', 'Intruder detected', 'detected.png')
        os.remove("detected.png")
    rawCapture.truncate(0)

cascadePath = "haarcascade_frontalface_default.xml"
camera = PiCamera()
camera.resolution = (160, 120)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(160, 120))

faceCascade = cv2.CascadeClassifier(cascadePath)

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    processImageFromCamera(frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

#creating database
import cv2, sys, numpy, os
import urllib
import cv2
import numpy as np
import imutils
#url="http://192.168.1.2:8080/shot.jpg"

haar_file = 'haarcascade_frontalface_default.xml'
datasets = 'datasets'  #All the faces data will be present this folder
sub_data = 'yashwin'     #These are sub data sets of folder, for my faces I've used my name

path = os.path.join(datasets, sub_data)
if not os.path.isdir(path):
    os.mkdir(path)
(width, height) = (130, 100)    # defining the size of images 


face_cascade = cv2.CascadeClassifier(haar_file)
# The program loops until it has 30 images of the face.
cam = cv2.VideoCapture(0)

count = 1
while count < 101:
    #imgPath=urllib.urlopen(url)
    #imgNp=np.array(bytearray(imgPath.read()),dtype=np.uint8)
    #img=cv2.imdecode(imgNp,-1)
    ret,img = cam.read()
    
    img = imutils.resize(img, width=400)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 4)
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        face = gray[y:y + h, x:x + w]
        face_resize = cv2.resize(face, (width, height))
        cv2.imwrite('%s/%s.png' % (path,count), face_resize)
    count += 1
    print count
	
    cv2.imshow('OpenCV', img)
    key = cv2.waitKey(10)
    if key == 27:
        break
cv2.destroyAllWindows()

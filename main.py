import cv2
import time
import urllib
import imutils
import subprocess
import numpy as np
import cv2, sys, numpy, os
import RPi.GPIO as GPIO

#url="http://192.168.1.2:8080/shot.jpg"
url= cv2.VideoCapture(0)

motor = 21
buzzer =20

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(motor,GPIO.OUT)
GPIO.setup(buzzer,GPIO.OUT)
GPIO.setup(26, GPIO.IN, pull_up_down = GPIO.PUD_UP)

size = 4
haar_file = 'haarcascade_frontalface_default.xml'
datasets = 'datasets'

print('Training...')
(images, labels, names, id) = ([], [], {}, 0)
for (subdirs, dirs, files) in os.walk(datasets):
    for subdir in dirs:
        names[id] = subdir
        subjectpath = os.path.join(datasets, subdir)
        for filename in os.listdir(subjectpath):
            path = subjectpath + '/' + filename
            label = id
            images.append(cv2.imread(path, 0))
            labels.append(int(label))
        id += 1
(width, height) = (130, 100)

(images, labels) = [numpy.array(lis) for lis in [images, labels]]

#model = cv2.face.createFisherFaceRecognizer()
model = cv2.createFisherFaceRecognizer()

model.train(images, labels)

face_cascade = cv2.CascadeClassifier(haar_file)
webcam = cv2.VideoCapture(0)
value=False


try:
    
        
    while True:
    
        
        if(GPIO.input(26)==0):
            
            value=True
            wait_time = 10
            auth = 0
            
            while value:
                print("capture")
                

                ret,im=url.read()                
                im = imutils.resize(im, width=400)
                cv2.imwrite('/var/www/html/pan.jpg', im)
                
                gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.3, 5)
                for (x,y,w,h) in faces:
                    cv2.rectangle(im,(x,y),(x+w,y+h),(255,255,0),2)
                    face = gray[y:y + h, x:x + w]
                    face_resize = cv2.resize(face, (width, height))
                    #Try to recognize the face
                    prediction = model.predict(face_resize)
                    cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 3)
                    
                    if prediction[1]<500:
                        cv2.putText(im,'%s - %.0f' % (names[prediction[0]],prediction[1]),(x-10, y-10), cv2.FONT_HERSHEY_PLAIN,1,(255, 0, 0))
                        print( names[prediction[0]]);
                        auth = 1
                        wait_time = 0
                        value=False
                        break
                    elif(wait_time < 1):
                        auth =2
                        value =False
                    else:
                        wait_time-=1
                        cv2.putText(im,'scanning',(x-10, y-10), cv2.FONT_HERSHEY_PLAIN,1,(0, 255, 0))
                        
                cv2.imshow('OpenCV', im)
                cv2.imwrite('/var/www/html/capture.jpg', im);
                cv2.imwrite('capture.jpg', im)
                key = cv2.waitKey(10) & 0xFF
                
                if key == 27:
                     break
                if(auth == 2):
                    cv2.imwrite('capture.jpg', im)
                    cv2.imwrite('/var/www/html/capture.jpg', im);
                    print("unauthorized user")
                    GPIO.output(buzzer,True)
                    subprocess.Popen("sudo python mail.py",shell=True).communicate()
                    time.sleep(1)
                    subprocess.Popen("sudo python sms.py",shell=True).communicate()
                    GPIO.output(buzzer,False)


                    
                    
                elif(auth == 1):
                    print("authorized user");
                    GPIO.output(motor,True)                    
                    #subprocess.Popen("sudo python mail.py",shell=True).communicate()                    
                    time.sleep(5)
                    GPIO.output(motor,False)

            
               
except:
     KeyboardInterrupt()
     cv2.destroyAllWindows()

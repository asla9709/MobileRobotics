# lane_follow.py

import time
import cv2
import numpy as np
import math
import serial


ser = serial.Serial('/dev/ttyACM0',9600)
ser.flushInput()

#take a picture
#os.system('fswebcam -r 1920x1080 -S 3 --jpeg 100 /home/pi/Desktop/Camera/%H%M%S.jpg')
video = cv2.VideoCapture('video.mp4')
video.open(0)
#cv2.namedWindow("display", cv2.WINDOW_NORMAL)
theta=0
lineCenter = 0
minLineLength = 5
maxLineGap = 10
time.sleep(0.1)
while 1:
    #ctr-c to quit
    hide , image = video.read()
    #image = frame.array
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 85, 85)
    cv2.Canny()
    #cv2.imshow("display", blurred)
    lines = cv2.HoughLinesP(edged,1,np.pi/180,10,minLineLength,maxLineGap)
    #if(lines !=None):
    if(lines.any()):
        #print (lines)
        for x in range(0, len(lines)):
            for x1,y1,x2,y2 in lines[x]:
                cv2.line(image,(x1,y1),(x2,y2),(0,255,0),2)
                theta=theta+math.atan2((y2-y1),(x2-x1))
    #print(theta)GPIO pins were connected to arduino for servo steering control
    threshold=6
    lineCenter = 160 - (2 * (10+theta))
    dataLine = "X{0}R{1}\n".format(lineCenter, 14)
    ser.write(dataLine.encode('utf-8'))
    print (theta)
    if(theta>threshold):
        print("left")
    if(theta<-threshold):
        print("right")
    if(abs(theta)<threshold):
        print ("straight")
    theta=0
    cv2.imshow("Frame",image)
    key = cv2.waitKey(1) & 0xFF
    #rawCapture.truncate(0)
    if key == ord("q"):
        break


# lane_detection.py

import cv2
import time
import cv2
import numpy as np
import math
import serial



ser = serial.Serial('/dev/ttyACM0',9600)
ser.flushInput()
#take a picture
#os.system('fswebcam -r 1920x1080 -S 3 --jpeg 100 /home/pi/Desktop/Camera/%H%M%S.jpg')
# Capture video from camera
width = 640
height = 480
Xcenter = width / 2
video = cv2.VideoCapture(0)
video.set(cv2.CAP_PROP_FRAME_WIDTH,width)
video.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
# Create a named window with opencv

#cv2.namedWindow("display", cv2.WINDOW_NORMAL)
theta=0
point_count = 0
x_sum = 0
y_sum = 0
minLineLength = 10
maxLineGap = 10
time.sleep(0.1)
line_detector = cv2.createLineSegmentDetector()
while 1:
    #ctr-c to quit
    hide , image = video.read()
    #image = frame.array
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 200, 195)
    #cv2.imshow("display", edged)
    lines = cv2.HoughLinesP(edged,1,np.pi/180,10,minLineLength,maxLineGap)
    #lines = line_detector.detect(edged)
    horizon = int(height / 2);
    #
    horizon = 300
    if(lines is not None and lines.any()):    
       #print (lines)
        cv2.line(image,(0,horizon),(600,horizon),(0,0,255),2)
        for x in range(0, len(lines)):
           for x1,y1,x2,y2 in lines[x]:
               if(y2 < horizon):
                   continue
               cv2.line(image,(x1,y1),(x2,y2),(0,255,0),2)
               cenX = int((x1 + x2) / 2)
               cenY = int((y1 + y2) / 2)
               #length = math.sqrt()
               x_sum += cenX
               y_sum += cenY
               point_count += 1
               
    #print(theta)
               #GPIO pins were connected to arduino for servo steering control
    threshold=6
    if (point_count > 0):
        avg_x = int(x_sum / point_count)
        avg_y = int(y_sum / point_count)
        cv2.circle(image, (avg_x, avg_y), 5, (0,0,255))
        print ("({}, {})".format(avg_x, avg_y))
        
        
        dataLine = "X{0}R{1}\n".format(avg_x, 8)
        ser.write(dataLine.encode('utf-8'))

    point_count = 0
    x_sum = 0
    y_sum = 0
    cv2.imshow("Frame",image)
    key = cv2.waitKey(1) & 0xFF
    #rawCapture.truncate(0)
    if key == ord("q"):
       break


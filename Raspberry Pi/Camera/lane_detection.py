# lane_detection.py

import time
import cv2
import numpy as np
import math


def calculate_line(line_1, line_2, point):
    if len(line_1) == 0:
        line_1.append(point)
    elif len(line_2) == 0:
        line_2.append(point)

#take a picture
#os.system('fswebcam -r 1920x1080 -S 3 --jpeg 100 /home/pi/Desktop/Camera/%H%M%S.jpg')
video = cv2.VideoCapture('video.mp4')
video.open(0)
#cv2.namedWindow("display", cv2.WINDOW_NORMAL)
theta=0
point_count = 1
x_sum = 0
y_sum = 0
minLineLength = 5
maxLineGap = 3
time.sleep(0.1)
while 1:
    #ctr-c to quit
    hide , image = video.read()
    #image = frame.array
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 200, 195)
    #cv2.imshow("display", edged)
    lines = cv2.HoughLinesP(edged,1,np.pi/180,10,minLineLength,maxLineGap)
    
    horizon = 240
    #if(lines !=None):
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
               x_sum += cenX
               y_sum += cenY
               point_count += 1
               
               theta=theta+math.atan2((y2-y1),(x2-x1))
    #print(theta)
               #GPIO pins were connected to arduino for servo steering control
    threshold=6
    avg_x = int(x_sum / point_count)
    avg_y = int(y_sum / point_count)
    cv2.circle(image, (avg_x, avg_y), 5, (0,0,255))
    print ("({}, {})".format(avg_x, avg_y))
    #print("h: {}".format(len(image)), "w: {}".format(len(image[0])))
    comment = '''if(theta>threshold):
       print("left")
    if(theta<-threshold):
       print("right")
    if(abs(theta)<threshold):
      print ("straight")
    '''
    theta=0
    point_count = 1
    x_sum = 0
    y_sum = 0
    cv2.imshow("Frame",image)
    key = cv2.waitKey(1) & 0xFF
    #rawCapture.truncate(0)
    if key == ord("q"):
       break


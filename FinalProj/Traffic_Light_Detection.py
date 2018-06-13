# Lab 5 sample program for tracking an object with a specific color
# use the trackbar to select the HSV range for the target color

import cv2
import numpy as np
import serial
import math

def detect_stoplight(image):
    Hmax, Hmin, Smax, Smin, Vmax, Vmin = 12, 0, 255, 164, 255, 70
    
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, (Hmin,Smin,Vmin), (Hmax,Smax,Vmax))
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]

    if len(cnts) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)


        # only proceed if the radius meets a minimum size
        if radius > 10:
            # dataLine = "X{0}R{1}\n".format(x,radius)
            # ser.write(dataLine.encode('utf-8'))
            # print(math.floor(0.5*(y-180)),math.floor(0.5*(x-160)))
            # print(x, ", ", y, ",", radius)
            print("STOP")
            return True #Stoplight detected
        else:
            # ser.write("X-1Y-1\n".encode('utf-8'))
            # ser.write("X-1R-1\n".encode('utf-8'))
            print("GO")
            return False #no stoplight detected

ser = serial.Serial('/dev/ttyACM0',9600)
ser.flushInput()

# Callback function which does nothing for trackbar move
def nothing(x):
    pass

# Capture video from camera
width = 320
height = 240
Xcenter = width / 2
cp = cv2.VideoCapture(0)
cp.set(cv2.CAP_PROP_FRAME_WIDTH,width)
cp.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
# Create a named window with opencv
cv2.namedWindow('image')

# Initialize H, S, V values
Hmax, Hmin, Smax, Smin, Vmax, Vmin = 12, 0, 255, 164, 255, 70

# create trackbars for color change
cv2.createTrackbar('Hmax','image',Hmax,255,nothing)
cv2.createTrackbar('Hmin','image',Hmin,255,nothing)
cv2.createTrackbar('Smax','image',Smax,255,nothing)
cv2.createTrackbar('Smin','image',Smin,255,nothing)
cv2.createTrackbar('Vmax','image',Vmax,255,nothing)
cv2.createTrackbar('Vmin','image',Vmin,255,nothing)

# create switch for ON/OFF functionality, swtich button for mask window
switch = '0 : OFF \n1 : ON'
cv2.createTrackbar(switch, 'image',0,1,nothing)



while True:
    imgReadSuccessful,img = cp.read()
    
    detect_stoplight(img)

    # get current positions of four trackbars
    Hmax = cv2.getTrackbarPos('Hmax','image')
    Hmin = cv2.getTrackbarPos('Hmin','image')
    Vmax = cv2.getTrackbarPos('Vmax','image')
    Vmin = cv2.getTrackbarPos('Vmin','image')
    Smax = cv2.getTrackbarPos('Smax','image')
    Smin = cv2.getTrackbarPos('Smin','image')
    s = cv2.getTrackbarPos(switch,'image')

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, (Hmin,Smin,Vmin), (Hmax,Smax,Vmax))
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    if s:
        cv2.imshow('mask',mask)
    else:
        pass
        # cv2.destroyWindow('mask')

    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    #cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
    #center = None

    # only proceed if at least one contour was found
    #if len(cnts) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
     #   c = max(cnts, key=cv2.contourArea)
      #  ((x, y), radius) = cv2.minEnclosingCircle(c)


        # only proceed if the radius meets a minimum size
       # if 4 < radius < 6:
        #    dataLine = "X{0}R{1}\n".format(x,radius)
         #   ser.write(dataLine.encode('utf-8'))
            # print(math.floor(0.5*(y-180)),math.floor(0.5*(x-160)))
            # print(x, ", ", y, ",", radius)
          #  return True
       # else:
            #ser.write("X-1Y-1\n".encode('utf-8'))
        #    ser.write("X-1R-1\n".encode('utf-8'))
         #   return False

       # cv2.circle(img, (int(x), int(y)), int(radius),
        #                    (0, 255, 255), 2)

	# Press the Escape key to exit		
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break
    
    cv2.imshow('image',img)

cp.release()

cv2.destroyAllWindows()

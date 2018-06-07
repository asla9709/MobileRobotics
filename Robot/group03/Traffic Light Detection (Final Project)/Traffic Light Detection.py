# Sample program for tracking an object with a specific color
# use the trackbar to select the HSV range for the target color

import cv2
import numpy as np
import serial
import math

ser = serial.Serial('/dev/ttyACM0',9600)
ser.flushInput()

# Callback function which does nothing for trackbar move
def nothing(x):
    pass

# Capture video from camera
width = 200
height = 300
Xcenter = width / 2
cp = cv2.VideoCapture(0)
cp.set(cv2.CAP_PROP_FRAME_WIDTH,width)
cp.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
# Create a named window with opencv
cv2.namedWindow('image')
cv2.namedWindow('Frame', cv2.WINDOW_NORMAL)

# Initialize H, S, V values
RED = [208,0,255,139,255,120]
GREEN = [70,50,255,50,255,50]
rHmax,rHmin,rSmax,rSmin,rVmax,rVmin = RED
gHmax,gHmin,gSmax,gSmin,gVmax,gVmin = GREEN

# create trackbars for color change
#RED values
cv2.createTrackbar('rHmax','image',rHmax,255,nothing)
cv2.createTrackbar('rHmin','image',rHmin,255,nothing)
cv2.createTrackbar('rSmax','image',rSmax,255,nothing)
cv2.createTrackbar('rSmin','image',rSmin,255,nothing)
cv2.createTrackbar('rVmax','image',rVmax,255,nothing)
cv2.createTrackbar('rVmin','image',rVmin,255,nothing)
#GREEN values
cv2.createTrackbar('gHmax','image',gHmax,255,nothing)
cv2.createTrackbar('gHmin','image',gHmin,255,nothing)
cv2.createTrackbar('gSmax','image',gSmax,255,nothing)
cv2.createTrackbar('gSmin','image',gSmin,255,nothing)
cv2.createTrackbar('gVmax','image',gVmax,255,nothing)
cv2.createTrackbar('gVmin','image',gVmin,255,nothing)

# create switch for ON/OFF functionality, swtich button for mask window
rswitch = '0 : rOFF \t1 : rON'
gswitch = '0 : gOFF \t1 : gON'
cv2.createTrackbar(rswitch, 'image',0,1,nothing)
cv2.createTrackbar(gswitch, 'image',0,1,nothing)

while True:
    imgReadSuccessful,img = cp.read()

    # get current positions of four trackbars
    #RED values
    rHmax = cv2.getTrackbarPos('rHmax','image')
    rHmin = cv2.getTrackbarPos('rHmin','image')
    rVmax = cv2.getTrackbarPos('rVmax','image')
    rVmin = cv2.getTrackbarPos('rVmin','image')
    rSmax = cv2.getTrackbarPos('rSmax','image')
    rSmin = cv2.getTrackbarPos('rSmin','image')
    rs = cv2.getTrackbarPos(rswitch,'image')
    #GREEN values
    gHmax = cv2.getTrackbarPos('gHmax','image')
    gHmin = cv2.getTrackbarPos('gHmin','image')
    gVmax = cv2.getTrackbarPos('gVmax','image')
    gVmin = cv2.getTrackbarPos('gVmin','image')
    gSmax = cv2.getTrackbarPos('gSmax','image')
    gSmin = cv2.getTrackbarPos('gSmin','image')
    gs = cv2.getTrackbarPos(gswitch,'image')

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    rmask = cv2.inRange(hsv, (rHmin,rSmin,rVmin), (rHmax,rSmax,rVmax))
    rmask = cv2.erode(rmask, None, iterations=1)
    rmask = cv2.dilate(rmask, None, iterations=1)
    gmask = cv2.inRange(hsv, (gHmin,gSmin,gVmin), (gHmax,gSmax,gVmax))
    gmask = cv2.erode(gmask, None, iterations=1)
    gmask = cv2.dilate(gmask, None, iterations=1)

    if rs:
        cv2.imshow('rmask',rmask)
    else:
        pass
        #cv2.destroyWindow('rmask')
    if gs:
        cv2.imshow('gmask',gmask)
    else:
        pass
        #cv2.destroyWindow('gmask')

    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    rcnts = cv2.findContours(rmask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
    gcnts = cv2.findContours(gmask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None

    # only proceed if at least one contour was found
    if len(rcnts) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c = max(rcnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        
    if len(gcnts) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c = max(gcnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        
        # only proceed if the radius meets a minimum size
    if radius > 6:
            dataLine = "X{0}Y{0}".format(x,y)
            ser.write(dataLine.encode('utf-8'))
        # # draw the circle and centroid on the frame,
        # # then update the list of tracked points
        #     cv2.circle(img, (int(x), int(y)), int(radius),
        #                    (0, 255, 255), 2)
        #     text = 'x:'+str(int(x))+'y:'+str(int(y))+'r:'+str(int(radius))
        #
        #     #cv2.putText(img,text,(int(x)-125,int(y)), cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0))
        #     ##PUT ON SERIAL

        # only proceed if the radius meets a minimum size
    #if radius > 10:
        # draw the circle and centroid on the frame,
        # then update the list of tracked points
     #   cv2.circle(img, (int(x), int(y)), int(radius),
       #                    (0, 255, 255), 2)
      #  text = 'x:'+str(int(x))+'y:'+str(int(y))+'r:'+str(int(radius))
        #create two variables for x position data and radius data
      #  xData = str(int(x)) + '/n';
      #  radiusData = str(int(radius)) + '/n';
        #send the x position and radius to the arduino for processing
      #  ser.write(xData.encode('ascii'));
       # ser.write(radiusData.encode('ascii'));
      #  cv2.putText(img,text,(int(x)-125,int(y)), cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0))

	# Press the Escape key to exit	
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

    cv2.imshow('Frame',img)
    k = cv2.waitKey(1) & 0xFF

cp.release()

cv2.destroyAllWindows()


# camera.py

import cv2

#take a picture
#os.system('fswebcam -r 1920x1080 -S 3 --jpeg 100 /home/pi/Desktop/Camera/%H%M%S.jpg')
video = cv2.VideoCapture('video.mp4')
video.open(0)
cv2.namedWindow("display", cv2.WINDOW_NORMAL)


while 1:
    #ctr-c to quit
    hide , img = video.read()
    hide = cv2.imshow('display', img)
    hide = cv2.waitKey(2)
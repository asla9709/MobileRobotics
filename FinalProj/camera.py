import math
import time
from threading import Thread

import cv2
import numpy as np

AUTO_SPEED = 50
AUTO_X_SCALE = 0.8

class Camera:
    def __init__(self):
        self.width = 640
        self.height = 480
        self.video = cv2.VideoCapture(0)
        self.video.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.video.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)

        self.horizon = int(self.height / 2)
        self.robot_left_side = 25
        self.robot_right_side = 475
        self.roi_height = int(self.height - self.horizon)
        self.robot_center = int((50 + 450) / 2)
        self.elipseKernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))

        self.suggested_move = (0, 0)
        self.stoplight_detected = False
        self.show_video = True
        self.debug = False
        self.image = 0

    def run_(self):
        while True:
            successful, image = self.video.read()
            if successful:
                self.stoplight_detected = self.detect_stoplight(image)
                if self.stoplight_detected:
                    self.suggested_move = (0,0)
                else:
                    self.suggested_move = self.detect_lanes(image)
                time.sleep(0.1)
            else:
                self.suggested_move = (0,0)

    def run(self):
        self.run_thread = Thread(target=self.run_)
        self.run_thread.start()

    def detect_stoplight(self, full_image):
        Hmax, Hmin, Smax, Smin, Vmax, Vmin = 12, 0, 255, 164, 255, 70

        hsv = cv2.cvtColor(full_image, cv2.COLOR_BGR2HSV)
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
                # print("STOP")
                return True #Stoplight detected
            else:
                # ser.write("X-1Y-1\n".encode('utf-8'))
                # ser.write("X-1R-1\n".encode('utf-8'))
                # print("GO")
                return False #no stoplight detected

    def detect_lanes(self, full_image):
        image = full_image[self.horizon:self.height, 0:self.width]
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5,5), 0)
        #parameters I found to giv the best filter
        edged = cv2.Canny(blurred, threshold1=0, threshold2=348)
        out = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, self.elipseKernel, iterations = 7)
        out, contour,hier = cv2.findContours(out,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)
        left_lane, right_lane = self.extract_lines(contour)

        if not left_lane is None and  not right_lane is None:
            x,y,w,h = cv2.boundingRect(left_lane)
            mid_left = math.floor(x + w/2)
            x, y, w, h = cv2.boundingRect(right_lane)
            mid_right = math.floor(x + w / 2)

            mid = math.floor((mid_left+mid_right)/2)
            xoffset = (mid - self.robot_center)

            cv2.circle(image, (math.floor(mid), 30), 5, (255,255,255))
            cv2.line(image,(mid_left,0),(mid_left,200),(255,255,255))
            cv2.line(image,(mid_right,0),(mid_right,200),(255,255,255))

        elif not left_lane is None:
            x,y,w,h = cv2.boundingRect(left_lane)
            mid_left = math.floor(x + w/2)

            xoffset = mid_left - self.robot_left_side

        elif not right_lane is None:
            x,y,w,h = cv2.boundingRect(right_lane)
            mid_right = math.floor(x + w/2)

            xoffset = mid_right - self.robot_right_side

        else:
            xoffset = 0

        xoffset = math.floor(xoffset)
        if self.debug:
            cv2.line(image, (self.robot_center,150), (self.robot_center + xoffset,150), (255,255,0))
            cv2.line(image,(self.robot_center, 0),(self.robot_center, self.roi_height),(0,0,255),2)
            cv2.line(image,(self.robot_left_side, 0),(self.robot_left_side, self.roi_height),(0,0,255),2)
            cv2.line(image,(self.robot_right_side, 0),(self.robot_right_side, self.roi_height),(0,0,255),2)

            cv2.imshow("Frame_3", image)
            key = cv2.waitKey(1) & 0xFF

        return(xoffset*AUTO_X_SCALE, AUTO_SPEED)



    def extract_lines(self, contours):
        count = len(contours)
        #print(np.minimum([contours[0]]))
        if count == 0:
            return None, None

        if count == 1:
            rect = cv2.minAreaRect(contours[0])
            angle = rect[2]
            if (rect[1][0] > rect[1][1]):
                angle = angle + 90

            if angle < 0:
                return None, contours[0]
            else:
                return contours[0], None

        if count == 2:
            first_average_x = np.mean([contours[0]], 1)[0][0][0]
            second_average_x = np.mean([contours[1]], 1)[0][0][0]
            #print(average_point)
            if first_average_x > second_average_x:
                return contours[1], contours[0]
            else:
                return contours[0], contours[1]

        if count > 2:
            left, right = contours[0], contours[0]
            for contour in contours:
                lowest_x = tuple(contour[contour[:, :, 1].argmax()][0])
                left_lowest_x = tuple(left[left[:, :, 1].argmax()][0])
                right_lowest_x = tuple(right[right[:, :, 1].argmax()][0])
                if abs(lowest_x[0] - self.robot_left_side) < abs(left_lowest_x[0] - self.robot_left_side):
                    left = contour
                elif abs(lowest_x[0] - self.robot_right_side) < abs(right_lowest_x[0] - self.robot_right_side):
                    right = contour
            return left, right


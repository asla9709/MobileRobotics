import time
from threading import Thread

import cv2
import numpy as np

AUTO_SPEED = 20
AUTO_X_SCALE = 1

class Camera:
    def __init__(self):
        self.width = 640
        self.height = 480
        self.video = cv2.VideoCapture(0)
        self.video.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.video.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)

        self.horizon = int(self.height / 2)
        self.robot_left_side = 50 / 2
        self.robot_right_side = 450 / 2
        self.roi_height = self.height - self.horizon
        self.robot_center = int((50 + 450) / 2)
        self.elipseKernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))

        self.suggested_move = (0, 0)
        self.stoplight_detected = False

    def run_(self):
        while True:
            #TODO take picture
            successful, image = self.video.read()
            self.stoplight_detected = self.detect_stoplight(image)
            if self.stoplight_detected:
                self.suggested_move = (0,0)
            else:
                self.suggested_move = self.detect_lanes(image)
            time.sleep(0.1)

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
        edged = cv2.Canny(blurred, threshold1=0, threshold2=400)
        out = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, self.elipseKernel, iterations = 7)
        out, contour,hier = cv2.findContours(out,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)
        left_lane, right_lane = self.extract_lines(contour)

        right_correction = left_correction = 0
        if left_lane is not None:
            left_point = tuple(left_lane[left_lane[:, :, 1].argmax()][0])
            #cv2.drawContours(image,[left_lane],0, (255, 0, 0),-1)
            #v2.circle(image, (left_point[0],left_point[1]), 5, (0, 0, 255))
            left_correction = int(left_point[0] - (self.robot_left_side- 25))
            #cv2.circle(image, (self.robot_center + left_correction, int(left_point[1])), 10, (0, 255, 255))

        if right_lane is not None:
            right_point = tuple(right_lane[right_lane[:, :, 1].argmax()][0])
            #cv2.drawContours(image,[right_lane],0, (0, 255, 0),-1)
            #cv2.circle(image, (right_point[0],right_point[1]), 5, (0, 0, 255))
            right_correction = int(right_point[0] - (self.robot_right_side + 25))
            #cv2.circle(image, (self.robot_center + right_correction, int(right_point[1])), 10, (0, 255, 255))

        if left_lane is not None or right_lane is not None:
            #cv2.circle(image, (self.robot_center + left_correction + right_correction, self.roi_height), 5, (0, 0, 255))
            #dataLine = "X{0}V{1}\n".format(self.robot_center + left_correction + right_correction, 15)
            return (AUTO_X_SCALE*(left_correction + right_correction), AUTO_SPEED)
        else:
            #dataLine = "X{0}V{1}\n".format(self.robot_center, 0)
            return (0, 0)


    def extract_lines(self, contours):
        count = len(contours)
        #print(np.minimum([contours[0]]))
        if count == 0:
            return None, None
        if count == 1:
            lowest_x =  tuple(contours[0][contours[0][:, :, 1].argmax()][0])

            if lowest_x > self.robot_center:
                return None, contours[0]
            else:
                return contours[0], None
        if count == 2:
            first_lowest_x = tuple(contours[0][contours[0][:, :, 1].argmax()][0])
            second_lowest_x =  tuple(contours[1][contours[1][:, :, 1].argmax()][0])
            #print(average_point)
            if first_lowest_x > second_lowest_x:
                return contours[1], contours[0]
            else:
                return contours[0], contours[1]
        if count > 2:
            left, right = contours[0]
            for contour in contours:
                lowest_x = tuple(contour[contour[:, :, 1].argmax()][0])
                left_lowest_x =  tuple(left[left[:, :, 1].argmax()][0])
                right_lowest_x =  tuple(right[right[:, :, 1].argmax()][0])
                if abs(lowest_x[0] - self.robot_left_side) < abs(left_lowest_x[0] - self.robot_left_side):
                    left = contour
                elif abs(lowest_x[0] - self.robot_right_side) < abs(right_lowest_x[0] - self.robot_right_side):
                    right = contour
            return left, right


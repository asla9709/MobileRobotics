import time
import cv2
import numpy as np
import math
import serial


font = cv2.FONT_HERSHEY_SIMPLEX

class Robot:
    def __init__(self):
        self.initialize_camera()
        # self.initialize_serial()
        
    
    def initialize_camera(self):
        self.width = 640
        self.height = 480
        self.Xcenter = self.width / 2
        self.video = cv2.VideoCapture(1)
        self.video.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.video.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        
        self.horizon = 300#int(self.height / 2)
        self.robot_left_side = 25
        self.robot_right_side = 475
        self.roi_height = self.height - self.horizon
        self.robot_center = int((50 + 450) / 2)
        self.initialize_edge_settings()
        
    def initialize_serial(self):
        self.ser = serial.Serial('/dev/ttyACM0',9600)
        self.ser.flushInput()
        
    def initialize_edge_settings(self):
        cv2.namedWindow("settings")
        #(value, count, onchange)
        cv2.createTrackbar('MinLineLength','settings',200,255,self.nothing)
        cv2.createTrackbar('MaxLineGap','settings',20,100,self.nothing)
        cv2.createTrackbar('Horizon','settings', self.robot_center,self.width,self.nothing)
        cv2.createTrackbar('reps','settings', 1, 100, self.nothing)
        cv2.createTrackbar('aeps','settings', 1, 100, self.nothing)
        cv2.createTrackbar('threshold1','settings', 0, 300, self.nothing)
        cv2.createTrackbar('threshold2','settings', 350, 1000, self.nothing)
        
    
    def lane_detection(self, follow = False):
        cv2.namedWindow("test")
        
        
        line_detector = cv2.createLineSegmentDetector()
        precison = np.array(1)
        dilateKernel = (1, 25)
        while 1:
            minLineLength = cv2.getTrackbarPos('MinLineLength','settings')
            maxLineGap = cv2.getTrackbarPos('MaxLineGap','settings')
            self.horizon = cv2.getTrackbarPos('Horizon','settings')
            reps = float(cv2.getTrackbarPos('reps','settings')) /100.0
            aeps = float(cv2.getTrackbarPos('aeps','settings')) /100.0
            threshold1 = cv2.getTrackbarPos('threshold1','settings')
            threshold2 = cv2.getTrackbarPos('threshold2','settings')
            
            hide , full_image = self.video.read()
            '''
            TODO: Detect Stoplight here
            '''
            
            image = full_image[self.horizon:self.height, 0:self.width]
            blank_image = np.zeros((self.height, self.width, 3), np.uint8)            
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            blurred = cv2.GaussianBlur(gray, (5,5), 0)
            
            
            #parameters I found to giv the best filter
            edged = cv2.Canny(blurred, threshold1, threshold2)
            
            ke = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
            #kc = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
            out = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, ke, iterations = 7)
            #out = cv2.dilate(edged, ke,iterations = 7)

            out, contour,hier = cv2.findContours(out,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)
            '''
            contour is an array of contours..
            where contour[0] is an array of points on the contour
            '''
            count = 0
            
            left_lane, right_lane = self.extract_lines(contour)

            if not left_lane is None and  not right_lane is None:
                x,y,w,h = cv2.boundingRect(left_lane)
                mid_left = math.floor(x + w/2)
                x, y, w, h = cv2.boundingRect(right_lane)
                mid_right = math.floor(x + w / 2)

                mid = math.floor((mid_left+mid_right)/2)

                cv2.circle(image, (math.floor(mid), 30), 5, (255,255,255))
                cv2.line(image,(mid_left,0),(mid_left,200),(255,255,255))
                cv2.line(image,(mid_right,0),(mid_right,200),(255,255,255))

                xoffset = (mid - self.robot_center)
                # self.suggested_move = (xoffset, 50)

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

            cv2.line(image, (self.robot_center,150), (self.robot_center + xoffset,150), (255,255,0))




            # right_correction = 0
            # left_correction = 0
            #
            # if left_lane is not None:
            #     cv2.drawContours(image,[left_lane],0, (255, 0, 0),-1)
            #     left_point = tuple(left_lane[left_lane[:, :, 1].argmax()][0])
            #     cv2.circle(image, (left_point[0],left_point[1]), 5, (0, 0, 255))
            #
            #     left_correction = int(left_point[0] - (self.robot_left_side- 25))
            #     cv2.circle(image, (self.robot_center + left_correction, int(left_point[1])), 10, (0, 255, 255))
            #     #if follow:
            #         #dataLine = "X{0}V{1}\n".format(self.robot_center + left_correction, 17)
            #         #self.ser.write(dataLine.encode('utf-8'))
            # if right_lane is not None:
            #     cv2.drawContours(image,[right_lane],0, (0, 255, 0),-1)
            #     right_point = tuple(right_lane[right_lane[:, :, 1].argmax()][0])
            #     cv2.circle(image, (right_point[0],right_point[1]), 5, (0, 0, 255))
            #
            #     right_correction = int(right_point[0] - (self.robot_right_side + 25))
            #     cv2.circle(image, (self.robot_center + right_correction, int(right_point[1])), 10, (0, 255, 255))
            #
            #     #if follow:
            #         #dataLine = "X{0}R{1}\n".format(self.robot_center + correction, 17)
            #         #self.ser.write(dataLine.encode('utf-8'))
            # if left_lane is not None or right_lane is not None:
            #     if follow:
            #         cv2.circle(image, (self.robot_center + left_correction + right_correction, self.roi_height), 5, (255, 0, 0))
            #         dataLine = "X{0}R{1}\n".format(self.robot_center - left_correction + right_correction, 15)
            #         # self.ser.write(dataLine.encode('utf-8'))
            # else:
            #     if follow:
            #         dataLine = "X{0}R{1}\n".format(self.robot_center, -1)
            #         # self.ser.write(dataLine.encode('utf-8'))
            
            cv2.line(image,(self.robot_center, 0),(self.robot_center, self.roi_height),(0,0,255),2)
            cv2.line(image,(self.robot_left_side, 0),(self.robot_left_side, self.roi_height),(0,0,255),2)
            cv2.line(image,(self.robot_right_side, 0),(self.robot_right_side, self.roi_height),(0,0,255),2)
            

            cv2.imshow("Frame_2", out)
            cv2.imshow("Frame_3", image)
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
               break
            
            
            
    def separate_lines(self, lines):
        """ Takes an array of hough lines and separates them by +/- slope.
            The y-axis is inverted in matplotlib, so the calculated positive slopes will be right
            lane lines and negative slopes will be left lanes. """
        right = []
        left = []
        for x1,y1,x2,y2 in lines[:, 0]:
            m = (float(y2) - y1) / (x2 - x1)
            if m >= 0: 
                right.append([x1,y1,x2,y2])
            else:
                left.append([x1,y1,x2,y2])
        
        return [right], [left]
    
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
    
    @staticmethod
    def nothing(x):
        pass

        
        
if __name__ == '__main__':
    robot = Robot()
    lane_follow = True
    robot.lane_detection(lane_follow)
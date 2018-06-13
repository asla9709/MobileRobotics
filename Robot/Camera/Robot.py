import time
import cv2
import numpy as np
import math
import serial


class Robot:
    def __init__(self):
        self.initialize_camera()
        self.initialize_serial()
        
    
    def initialize_camera(self):
        self.width = 640
        self.height = 480
        self.Xcenter = self.width / 2
        self.video = cv2.VideoCapture(0)
        self.video.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.video.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        
        self.horizon = 300#int(self.height / 2)
        self.robot_left_side = 50
        self.robot_right_side = 450
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
        cv2.createTrackbar('threshold2','settings', 400, 1000, self.nothing)
        
    
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
            
            #if  len(contour) == 2:
            left_lane, right_lane = self.extract_lines(contour)     
            ''''
            if left_lane is not None and right_lane is not None:
                cv2.drawContours(image,[left_lane],0, (255, 0, 0),-1)
                left_average = np.mean([left_lane], 1)[0][0]
                cv2.circle(image, (int(left_average[0]), int(left_average[1])), 5, (0, 0, 255))
                cv2.drawContours(image,[right_lane],0, (0, 255, 0),-1)
                right_average = np.mean([right_lane], 1)[0][0]
                cv2.circle(image, (int(right_average[0]), int(right_average[1])), 5, (0, 0, 255))
                
                x_avg = int((left_average[0] + right_average[0])/ 2)
                y_avg = int((left_average[1] + right_average[1])/ 2)
                cv2.circle(image, (x_avg, y_avg), 10, (255, 255, 0))
                
                if follow:
                    dataLine = "X{0}R{1}\n".format(x_avg, 14)
                    self.ser.write(dataLine.encode('utf-8'))
            '''
            right_correction = 0
            left_correction = 0
            if left_lane is not None:
                left_point = tuple(left_lane[left_lane[:, :, 1].argmax()][0])
                cv2.drawContours(image,[left_lane],0, (255, 0, 0),-1)
                cv2.circle(image, (left_point[0],left_point[1]), 5, (0, 0, 255))
                left_correction = int(left_point[0] - (self.robot_left_side- 25))
                cv2.circle(image, (self.robot_center + left_correction, int(left_point[1])), 10, (0, 255, 255))
                #if follow:
                    #dataLine = "X{0}V{1}\n".format(self.robot_center + left_correction, 17)
                    #self.ser.write(dataLine.encode('utf-8'))
            if right_lane is not None:
                right_point = tuple(right_lane[right_lane[:, :, 1].argmax()][0])
                cv2.drawContours(image,[right_lane],0, (0, 255, 0),-1)
                cv2.circle(image, (right_point[0],right_point[1]), 5, (0, 0, 255))
                right_correction = int(right_point[0] - (self.robot_right_side + 25))
                cv2.circle(image, (self.robot_center + right_correction, int(right_point[1])), 10, (0, 255, 255))
                
                #if follow:
                    #dataLine = "X{0}R{1}\n".format(self.robot_center + correction, 17)
                    #self.ser.write(dataLine.encode('utf-8'))
            if left_lane is not None or right_lane is not None:
                if follow:
                    cv2.circle(image, (self.robot_center + left_correction + right_correction, self.roi_height), 5, (0, 0, 255))
                    dataLine = "X{0}R{1}\n".format(self.robot_center + left_correction + right_correction, 15)
                    self.ser.write(dataLine.encode('utf-8'))
            else:
                if follow:
                    dataLine = "X{0}R{1}\n".format(self.robot_center, -1)
                    self.ser.write(dataLine.encode('utf-8'))
                '''vx,vy, x0, y0 = cv2.fitLine(contour[0], cv2.DIST_L12, 0, reps, aeps)
                m=600
                cv2.line(image, (x0-m*vx[0], y0-m*vy[0]), (x0+m*vx[0], y0+m*vy[0]), (255,0,255))
                average_point = np.mean([contour[0]], 1)[0][0]
                #print(average_point)
                cv2.circle(image, (int(average_point[0]), int(average_point[1])), 5, (255,0, 255))
                
                
                vx,vy, x0, y0 = cv2.fitLine(contour[1], cv2.DIST_L12, 0, reps, aeps)
                m=600
                cv2.line(image, (x0-m*vx[0], y0-m*vy[0]), (x0+m*vx[0], y0+m*vy[0]), (0,255,255))
                average_point = np.mean([contour[1]], 1)[0][0]
                #print(average_point)
                cv2.circle(image, (int(average_point[0]), int(average_point[1])), 5, (0, 255, 255))
                #print(leftLine)
                count += 1
                
                #print(cnt)
                '''
            
            cv2.line(image,(self.robot_center, 0),(self.robot_center, self.roi_height),(0,0,255),2)
            cv2.line(image,(self.robot_left_side, 0),(self.robot_left_side, self.roi_height),(0,0,255),2)
            cv2.line(image,(self.robot_right_side, 0),(self.robot_right_side, self.roi_height),(0,0,255),2)
            
            #opening = cv2.morphologyEx(edged, cv2.MORPH_OPEN, k)
            #one = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, ks, iterations = dIterations)
            #two = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, ke, iterations = dIterations)
            '''
            hough_lines = cv2.HoughLinesP(two,2,np.pi/180,10,minLineLength,maxLineGap)
            cv2.line(blank_image,(0,self.horizon),(self.width,self.horizon),(0,0,255),2)
            #lines = list()
            lines, a,b,c = line_detector.detect(two)
            line_detector.drawSegments(blank_image, lines)

            if hough_lines is not None:
            #print(b)
                right_lines, left_lines = self.separate_lines(hough_lines)
                for x in range(0, len(left_lines)):
                   for x1,y1,x2,y2 in left_lines[x]:
                       if(y2 < self.horizon):
                           #continue
                           pass
                       cv2.line(blank_image,(x1,y1),(x2,y2),(0,255,0),2)
                       
                for x in range(0, len(right_lines)):
                   for x1,y1,x2,y2 in right_lines[x]:
                       if(y2 < self.horizon):
                           pass#continue
                       cv2.line(blank_image,(x1,y1),(x2,y2),(255,0,255),2)
                                            
            #'''    
                #cv2.polylines(blank_image,  [points],  False,  (0, 255, 255))
            #line_detector.compareSegments((self.width, self.height), hough_lines, lines_2, blank_image)
            
            #blank_image, x_heading = self.draw_midpoint((self.width, self.height), blank_image, lines)
            #cv2.imshow("test",edged)
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
            average_x = np.mean([contours[0]], 1)[0][0][0]
            
            if average_x > self.robot_center:
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
            avg_point_list = list()
            
            for i in range(0, count):
                avg_point_list.append(np.mean([contours[i]], 1)[0][0])
                
            left = avg_point_list[0]
            right = avg_point_list[0]
            return_list = list()
            for point in avg_point_list:
                if abs(point[0] - self.robot_left_side) < abs(left[0] - self.robot_left_side):
                    left = point
                if abs(point[0] - self.robot_right_side) < abs(right[0] - self.robot_right_side):
                    right = point
            
            for i in range(0, count):
                if (avg_point_list[i][0] == left[0] and avg_point_list[i][1] == left[1]) or (avg_point_list[i][0] == right[0] and avg_point_list[i][0] == right[0]):
                    return_list.append(contours[i])
            return self.extract_lines(return_list) #recursive                
    
    @staticmethod
    def nothing(x):
        pass

        
        

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
        self.initialize_edge_settings()
        self.horizon = 300#int(self.height / 2)
        
    def initialize_serial(self):
        self.ser = serial.Serial('/dev/ttyACM0',9600)
        self.ser.flushInput()
        
    def initialize_edge_settings(self):
        cv2.namedWindow("settings")
        #(value, count, onchange)
        cv2.createTrackbar('MinLineLength','settings',200,255,self.nothing)
        cv2.createTrackbar('MaxLineGap','settings',200,255,self.nothing)
    
    def lane_detection(self, follow = False):
        line_detector = cv2.createLineSegmentDetector()
        
        minLineLength = 5
        maxLineGap = 3
        horizon = int(self.height / 2)
        precison = np.array(1)
        while 1:
            minLineLength = cv2.getTrackbarPos('MinLineLength','settings')
            maxLineGap = cv2.getTrackbarPos('MaxLineGap','settings')
            
            hide , image = self.video.read()
            blank_image = np.zeros((self.height, self.width, 3), np.uint8)            
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            edged = cv2.Canny(blurred, 200, 195)
            
            
            #cv2.line(blank_image,(0,horizon),(600,horizon),(0,0,255),2)
            #lines = list()
            lines, a,b,c = line_detector.detect(edged)
            line_detector.drawSegments(blank_image, lines)
            hough_lines = cv2.HoughLinesP(edged,2,np.pi/180,10,minLineLength,maxLineGap)
            if hough_lines is not None:
            #print(b)
                points = list()
                for x in range(0, len(hough_lines)):
                   for x1,y1,x2,y2 in hough_lines[x]:
                       if(y2 < self.horizon):
                           continue
                       cv2.line(blank_image,(x1,y1),(x2,y2),(0,255,0),2)
                       points.append((x1, y1))
                       
                points = np.asarray(points)
                #cv2.polylines(blank_image,  [points],  False,  (0, 255, 255))
            #line_detector.compareSegments((self.width, self.height), hough_lines, lines_2, blank_image)
            
            #blank_image, x_heading = self.draw_midpoint((self.width, self.height), blank_image, lines)
            cv2.imshow("Frame",blank_image)
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
               break
            
            if follow:
                dataLine = "X{0}R{1}\n".format(x_heading, 16)
                self.ser.write(dataLine.encode('utf-8'))
            

    def draw_midpoint(self, size, image, lines):
        img_width = size[0]
        img_height = size[1]
        
        x_point_count = 0
        
        delta_max = 18
        x_points = list()
        
        prev_midpoint = int(img_width / 2)
        for y in reversed(range(img_height - 35, img_height-5)):
            #print("y: ", y)
            point_count = 0
            x_sum = 0
            l_avg = 0
            r_avg = 0
            if y < self.horizon:
                continue
            for x in range(0, img_width):
                b,g,r = image[y][x]
                if (b + g + r) > 100 and y > self.horizon:
                    x_sum += x
                    point_count += 1
                    if x == prev_midpoint:
                        x_sum = 0
                        point_count = 0
                    elif x < prev_midpoint:
                        l_avg = x_sum / point_count
                    else:
                        r_avg = x_sum / point_count
                    
            avg_x = int((l_avg + r_avg) / 2)
            prev_midpoint = avg_x
            x_points.append(avg_x)
            x_point_count += 1
            cv2.circle(image, (avg_x, y), 1, (0,255,0))
            #cv2.imshow("Frame",image)
        sum = 0
        count = len(x_points)
        for point in range(0, len(x_points)):
            sum +=  x_points[point]
        
        average = int(sum / count)
        sum = 0
        for point in range(0, len(x_points)):
            if abs(average - x_points[point]) > delta_max:
                count -= 1
            else:
                sum +=  x_points[point]
        if count == 0:
            heading = prev_midpoint
        else:
            heading = int(sum / count)
        cv2.circle(image, (heading, 440), 10, (0,255,255))
        return image, heading
    @staticmethod
    def nothing(x):
        pass

        
        

import time
import sys
sys.path.insert(1, './feedback_system')
sys.path.insert(2, './control_system')
from common import *
from table import Table
from PID.p_controller import P_Controller
from PID.pid_controller import PIDController
from data.cellDatabase import *
from feedback_system.findTable import *
from feedback_system.tracker import Tracker
from feedback_system.detector import Detector
import numpy as np
import cv2 as cv
import argparse
import imutils
import numpy as np

myTable = Table(cellDatabase)
parser = argparse.ArgumentParser()
parser.add_argument('--input', type=str,
                    help='Path to a video or a sequence of image.', default='data/videos/9.mp4')
parser.add_argument('--algo', type=str,
                    help='Background subtraction method (KNN, MOG2, COLOR).', default='COLOR')
parser.add_argument('--train', type=str,
                    help='Path to a video or a sequence of image.', default='data/videos/2.mp4')
args = parser.parse_args()

if args.algo == 'MOG2':
    detector = Detector(type="MOG2")
elif args.algo == 'KNN':
    detector = Detector(type="KNN")
elif args.algo == 'COLOR':
    lower_blue = np.array([100, 50, 50])
    upper_blue = np.array([130, 255, 255])
    detector = Detector(type="COLOR", color=(lower_blue, upper_blue))

tracker = Tracker(160, 30, 10, 100)
track_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0),
                (0, 255, 255), (255, 0, 255), (255, 127, 255),
                (127, 0, 255), (127, 0, 127)]

#capture = cv.VideoCapture(cv.samples.findFileOrKeep(args.input))
capture = cv.VideoCapture('http://192.168.43.1:8080/video')
if not capture.isOpened:
    print('Unable to open: ' + args.input)
    exit(0)

frames = 0
inf = 999999991
corners = [[0, 0], [inf, 0], [inf, inf], [0, inf]]

index = 0

pastPos = (0, 0) # xpast, ypast
dir = 1 # direction of rotate
hang = 0
hangFrames = 0

endAngle = 90
kp = 0.36
ki = 0.40
kd = 0.4
umax = 150 # max controller output, (N)
alpha = 0.8 # derivative filter smoothing factor
pid = PIDController(kp = kp, ki = ki, kd = kd, max_windup = 200, u_bounds
        = [-umax, umax], alpha = alpha)

pid.setTarget(endAngle)

goOut = 0
count = 0
t = 0
y0 =0
y1 = 0
fps = 25
fRotate = 1

waitBox = 0

def pointFromBezier(p, t):
    
    point = []
    point.append( ((1-t) ** 3)*p[0][0] + ((1-t)**2)*3*t * \
        p[1][0] + (1-t)*3*t*t*p[2][0] + (t**3)*p[3][0])

    point.append( ((1-t) ** 3)*p[0][1] + ((1-t)**2)*3*t * \
        p[1][1] + (1-t)*3*t*t*p[2][1] + (t**3)*p[3][1] )

    return point


# points = [tuple(map(int, p.split(','))) for p in points]
locations1 = []
# for t in np.arange(0.0, 1.2, 0.2):
#     locations1.append(pointFromBezier(points, t))
#     print (t)
print (locations1)
locations = [pixelToMmList([x,y], 640, 480) for [x,y] in locations1]
loc = myTable.getCellByLocation([2,0]).coordinates
locations = [loc]
print(locations)

cornersList = []
while True:
    keyboard = cv.waitKey(1)
    if keyboard == 'q' or keyboard == 27:
        for i in range(20):
            comCells = myTable.getCommonCells(myTable.cells[i])
            myTable.cells[i].stop(comCells)
        time.sleep(.2)
        break
    ret, frame = capture.read()
    if frame is None:
        break
    
    
    #frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    frames = frames + 1
    if frames < 50:
        corners1 = getCorners(frame)
        cornersList.append(corners1)
        continue

    if frames < 120:
        continue

    if frames == 120:
        cornersMean = np.mean(cornersList, axis=0)
        cornersStd = np.std(cornersList, axis=0)
        for i in range(len(cornersList)):
            for j in range(len(cornersList[0])):
                for k in range(len(cornersList[0][0])):
                    std = cornersStd[j][k]
                    mean = cornersMean[j][k]
                    if (cornersList[i][j][k] < mean - 2*std) or (cornersList[i][j][k] > mean + 2*std) : 
                        cornersList[i][j][k] = mean

        corners = np.mean(cornersList, axis=0)
    frame = getTableFromFrame(corners, frame)
    (centers, angles) = detector.Detect(frame)
    h1, w1 = frame.shape[:2]

    if waitBox:
        waitBox -= 1
        for i in range(20):
            comCells = myTable.getCommonCells(myTable.cells[i])
            myTable.cells[i].stop(comCells)
        continue
        
    
    if len(centers) == 0:
        continue
    
    
    centersMM = pixelToMm((float(centers[0][0]), float(centers[0][1])), w1, h1)
    angle = angles[0][0]

    h = [hang, hangFrames, dir]

    if index == -1:
        index = 0
        waitBox = 30
    [index, hang, hangFrames] = myTable.followPath(locations, centersMM, angle, index, h)
    
    if hang: 
        pass


    curPos = (centers[0][0], centers[0][1])
    [hang, hangFrames, dir] = myTable.isHanging(hang, hangFrames, curPos, pastPos, dir)
    
    pastPos = curPos
    
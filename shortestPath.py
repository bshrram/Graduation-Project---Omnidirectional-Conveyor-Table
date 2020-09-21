import time
import sys
sys.path.insert(1, './feedback_system')
sys.path.insert(2, './control_system')
from common import *

from feedback_system.findTable import *
from feedback_system.tracker import Tracker
from feedback_system.detector import Detector
from PID.pid_controller import PIDController
import numpy as np
import cv2 as cv
import argparse
import imutils
from PathPlanning import *

parser = argparse.ArgumentParser()
parser.add_argument('--input', type=str,
                    help='Path to a video or a sequence of image.', default='data/videos/9.mp4')
parser.add_argument('--algo', type=str,
                    help='Background subtraction method (KNN, MOG2, COLOR).', default='COLOR')
parser.add_argument('--train', type=str,
                    help='Path to a video or a sequence of image.', default='data/videos/2.mp4')
args = parser.parse_args()


if args.algo == 'COLOR':
    lower_blue = np.array([100, 50, 50])
    upper_blue = np.array([140, 255, 255])
    lower_black = np.array([95,45, 45 ])
    upper_black = np.array([140, 255, 255])
    detector = Detector(type="COLOR", color=(lower_blue, upper_blue))


def followshortestPath(myTable, cell1, cell2):
    cell1 = [int(i) for i in cell1]
    cell2 = [int(i) for i in cell2]

    tracker = Tracker(160, 30, 10, 100)
    track_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0),
                    (0, 255, 255), (255, 0, 255), (255, 127, 255),
                    (127, 0, 255), (127, 0, 127)]
    detectorqr = cv.QRCodeDetector()
    #capture = cv.VideoCapture(cv.samples.findFileOrKeep(args.input))
    capture = cv.VideoCapture('http://192.168.43.1:8080/video')
    if not capture.isOpened:
        print('Unable to open: ' + args.input)
        exit(0)
    r= False
    frames = 0
    inf = 999999991
    corners = [[0, 0], [inf, 0], [inf, inf], [0, inf]]
    locations = pathCoordinates(dijPath(4, 10, cell1, cell2 ), myTable)
    endCells = list(map(myTable.getCellByLocation, locations))
    locations = smooth(locations)



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

    waitBox = 0
    count = 0
    t = 0
    y0 =0
    y1 = 0
    fps = 25
    fRotate = 1
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
        # frame = cv.resize(frame, (640, 360))
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
        if len(centers) == 0:
            continue

        if waitBox:
            waitBox -= 1
            for i in range(20):
                comCells = myTable.getCommonCells(myTable.cells[i])
                myTable.cells[i].stop(comCells)
            continue
        
        centersMM = pixelToMm((float(centers[0][0]), float(centers[0][1])), w1, h1)
        angle = angles[0][0]

        h = [hang, hangFrames, dir]

        if index == -1:
            cell = myTable.getCellsByNearLocation(centersMM, 1)[0]
            waitBox = 30
            index = 0

        [index, hang, hangFrames] = myTable.followPath(locations, centersMM, angle, index, h)
        if hang: 
            continue


        curPos = (centers[0][0], centers[0][1])
        [hang, hangFrames, dir] = myTable.isHanging(hang, hangFrames, curPos, pastPos, dir)
        pastPos = curPos
        

        # if (len(centers) > 0):
        #     tracker.Update(centers)

        # for i in range(len(tracker.tracks)):
        #     if (len(tracker.tracks[i].trace) > 1):
        #         for j in range(len(tracker.tracks[i].trace)-1):
        #             # Draw trace line
        #             x1 = tracker.tracks[i].trace[j][0][0]
        #             y1 = tracker.tracks[i].trace[j][1][0]
        #             x2 = tracker.tracks[i].trace[j+1][0][0]
        #             y2 = tracker.tracks[i].trace[j+1][1][0]
        #             clr = tracker.tracks[i].track_id % 9
        #             cv.line(frame, (int(x1), int(y1)), (int(x2), int(y2)),
        #                     track_colors[clr], 2)

        # l = len(tracker.tracks[i].trace)
        # if (l > 1):
        #     xcur = tracker.tracks[0].trace[l-1][0][0]
        #     ycur = tracker.tracks[0].trace[l-1][1][0]
        #     xp = tracker.tracks[0].trace[l-2][0][0]
        #     yp = tracker.tracks[0].trace[l-2][1][0]
        #     dis = calculateDistance((xcur, ycur), (xp, yp))
        #     if (ref < 10):
        #         count+=1
        #     else:
        #         count = 0

        # # Display the resulting tracking frame
        #cv.imshow('Tracking', frame)

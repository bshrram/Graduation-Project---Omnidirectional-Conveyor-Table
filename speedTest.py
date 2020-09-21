import numpy as np
import cv2 as cv
import argparse
import imutils
import sys
sys.path.insert(1, './feedback_system')
sys.path.insert(2, './control_system')
from feedback_system.detector import Detector
from feedback_system.tracker import Tracker
from feedback_system.findTable import *
from table import Table
from data.cellDatabase import *
from PID.pid_controller import PIDController
from PID.p_controller import P_Controller
from common import *
import time
parser = argparse.ArgumentParser()
parser.add_argument('--input', type=str,
                    help='Path to a video or a sequence of image.', default='data/videos/9.mp4')
parser.add_argument('--algo', type=str,
                    help='Background subtraction method (KNN, MOG2, COLOR).', default='COLOR')
parser.add_argument('--train', type=str,
                    help='Path to a video or a sequence of image.', default='data/videos/2.mp4')
args = parser.parse_args()

if args.algo == 'MOG2':
    detector = Detector(type = "MOG2")
elif args.algo == 'KNN':
    detector = Detector(type ="KNN")
elif args.algo == 'COLOR':
    lower_blue = np.array([105,50,50])
    upper_blue = np.array([130,255,255])
    detector = Detector(type="COLOR", color= (lower_blue, upper_blue))

tracker = Tracker(160, 30, 10, 100)
track_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0),
                    (0, 255, 255), (255, 0, 255), (255, 127, 255),
                    (127, 0, 255), (127, 0, 127)]

#capture = cv.VideoCapture(cv.samples.findFileOrKeep(args.input))
capture = cv.VideoCapture('http://192.168.43.1:8080/video')
if not capture.isOpened:
    print('Unable to open: ' + args.input)
    exit(0)

frames =0
fps = 25
inf = 99999999
corners = [[0,0], [inf, 0], [inf, inf], [0, inf]]
myTable = Table(cellDatabase)
locations = [[2,0]]
endCells =list( map(myTable.getCellByLocation, locations))
index = 0
rot = False

count = 0
ref = 0
xp, yp = (0, 0)
b = 0
t = 0
tm = 0

endAngle = 90
y0 =0
y1 = 0
kp = 0.36
ki = 0.40
kd = 0.4

umax = 150 # max controller output, (N)
alpha = 0.8 # derivative filter smoothing factor
pid = PIDController(kp = kp, ki = ki, kd = kd, max_windup = 200, u_bounds
        = [-umax, umax], alpha = alpha)
pid.setTarget(endAngle)

p = P_Controller(kp = kp)
p.setTarget(endAngle)
goOut = 0

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
    if frames < 40:
        corners1 = getCorners(frame)
        corners[0][0] = max(corners[0][0], corners1[0][0])
        corners[0][1] = max(corners[0][1], corners1[0][1])
        corners[1][0] = min(corners[1][0], corners1[1][0])
        corners[1][1] = max(corners[1][1], corners1[1][1])
        corners[2][0] = min(corners[2][0], corners1[2][0])
        corners[2][1] = min(corners[2][1], corners1[2][1])
        corners[3][0] = max(corners[3][0], corners1[3][0])
        corners[3][1] = min(corners[3][1], corners1[3][1])
        
        # print(corners1)
        continue
    if frames < 100:
        continue
    tm += 1/fps
    corners = np.float32(corners)
    frame = getTableFromFrame(corners, frame)
    (centers, angles) = detector.Detect(frame)
    h1, w1 = frame.shape[:2]
    if len(centers) == 0:
        continue

    centersMM = pixelToMm((float(centers[0][0]), float(centers[0][1])), w1, h1)
    if frames == 100:
        (x0, y0) = centersMM
    angle = angles[0][0]
    runningCells = myTable.getCellsByNearLocation(centersMM, 4)
    if calculateDistance(centersMM, endCells[index].coordinates) < 40 and not goOut:
        
        if not rot:
            for i in range(20):
                comCells = myTable.getCommonCells(myTable.cells[i])
                myTable.cells[i].stop(comCells)
        rot = True
        index = (index+1) %len(locations)
    else:
        rot = False

    

    if (rot):
        w = endAngle - angle
        print(angle, endAngle)
        # print (w)
        # print(f"rotating {endCells[index].location}")
        if (abs(w)< 8):
            count += 1
            if (count>15):
                goOut = 1
                rot = 0
                continue
        else:
            count = 0
        
        
        # time step, (sec)

        dt = t - pid.last_timestamp_
        # Control effort
        u = pid.update(y0,t)
        
        y1dot = u
        y1 += y1dot*dt
        
        y0 = angle
        if u<0:
            u = max(-umax, min(-50, u))
        else :
            u = max(50, min(umax, u))
        print (u)
        myTable.move(endCells[index], 0, 0, -u)
        t+=1/fps
        [x, y] = endCells[index].location 

        # dx = [-1, 1, 0]
        # if x%2 ==1:
        #     dy = [0, 0, 1]
        # else:
        #     dy = [-1, -1, 1]
        # rotatingCells = []
        # for i in range(len(dx)):
        #     cell = myTable.getCellByLocation([x + dx[i], y+ dy[i]])
        #     if cell is not None:
        #         rotatingCells.append(cell)
        
        # for i in range(len(rotatingCells)):
        #     if rotatingCells[i].id == endCells[index].id:
        #         continue
        #     myTable.move(rotatingCells[i], 0, 0, -w)

    if goOut: 
        y0 = 163.75
        x0 = 165.8
        dy = 157.5
        dx = 90.93 * 2
        cell = runningCells[0]
        loc = (cell.coordinates[0]+ 200, cell.coordinates[1])
        myTable.goToLocation(loc, centersMM)
        if calculateDistance(centersMM, loc) < 50:
            for i in range(20):
                comCells = myTable.getCommonCells(myTable.cells[i])
                myTable.cells[i].stop(comCells)
            time.sleep(.2)
            break
        continue

    if (not rot):
        goOut = 0
        # print (f"going to: {endCells[index].location}")
        d = calculateDistance((xp, yp), centersMM)
        v = d*fps
        print (f"d: {d}, tm: {tm},  v: {v}")
        print( f"xp, yp: {(xp,yp)}")
        (xp, yp) = centersMM
        myTable.goToCell(endCells[index], centersMM)

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
    #     ref = dis - ref
    #     print (ref)
    #     if (ref < 10):
    #         count+=1
    #     else:
    #         count = 0
    
    # # Display the resulting tracking frame
    cv.imshow('Tracking', frame)

    

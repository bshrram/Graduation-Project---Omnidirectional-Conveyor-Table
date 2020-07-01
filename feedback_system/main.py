import numpy as np
import cv2 as cv
import argparse
import imutils
from detector import Detector
from tracker import Tracker
from findTable import *

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
capture = cv.VideoCapture('http:192.168.1.112:8080/video')
if not capture.isOpened:
    print('Unable to open: ' + args.input)
    exit(0)

frames =0
inf = 99999999
corners = [[0,0], [inf, 0], [inf, inf], [0, inf]]
while True:
    ret, frame = capture.read()
    if frame is None:
        break
    # frame = cv.resize(frame, (640, 360))
    #frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    frames = frames + 1
    if frames < 50:
        corners1 = getCorners(frame)
        corners[0][0] = max(corners[0][0], corners1[0][0])
        corners[0][1] = max(corners[0][1], corners1[0][1])
        corners[1][0] = min(corners[1][0], corners1[1][0])
        corners[1][1] = max(corners[1][1], corners1[1][1])
        corners[2][0] = min(corners[2][0], corners1[2][0])
        corners[2][1] = min(corners[2][1], corners1[2][1])
        corners[3][0] = max(corners[3][0], corners1[3][0])
        corners[3][1] = min(corners[3][1], corners1[3][1])
        
        print(corners1)
        continue
    
    corners = np.float32(corners)
    frame = getTableFromFrame(corners, frame)
    centers = detector.Detect(frame)
    if (len(centers) > 0):
        tracker.Update(centers)

    for i in range(len(tracker.tracks)):
        if (len(tracker.tracks[i].trace) > 1):
            for j in range(len(tracker.tracks[i].trace)-1):
                # Draw trace line
                x1 = tracker.tracks[i].trace[j][0][0]
                y1 = tracker.tracks[i].trace[j][1][0]
                x2 = tracker.tracks[i].trace[j+1][0][0]
                y2 = tracker.tracks[i].trace[j+1][1][0]
                clr = tracker.tracks[i].track_id % 9
                cv.line(frame, (int(x1), int(y1)), (int(x2), int(y2)),
                        track_colors[clr], 2)

    # Display the resulting tracking frame
    cv.imshow('Tracking', frame)

    keyboard = cv.waitKey(10)
    if keyboard == 'q' or keyboard == 27:
        break


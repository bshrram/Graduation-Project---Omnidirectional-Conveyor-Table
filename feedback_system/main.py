import numpy as np
import cv2 as cv
import argparse
from detector import Detector
from tracker import Tracker
from findTable import *

parser = argparse.ArgumentParser()
parser.add_argument('--input', type=str,
                    help='Path to a video or a sequence of image.', default='data/videos/14.mp4')
parser.add_argument('--algo', type=str,
                    help='Background subtraction method (COLOR).', default='COLOR')
args = parser.parse_args()


if args.algo == 'COLOR':
    lower_blue = np.array([110,100,100])
    upper_blue = np.array([120,255,255])
    detector = Detector(type="COLOR", color= (lower_blue, upper_blue))

tracker = Tracker(160, 30, 10, 100)
track_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0),
                    (0, 255, 255), (255, 0, 255), (255, 127, 255),
                    (127, 0, 255), (127, 0, 127)]

capture = cv.VideoCapture(cv.samples.findFileOrKeep(args.input))
# capture = cv.VideoCapture('http:192.168.1.106:8080/video')
if not capture.isOpened:
    print('Unable to open: ' + args.input)
    exit(0)

frames = 0
inf = 99999999
corners = [[0,0], [inf, 0], [inf, inf], [0, inf]]
while True:
    ret, frame = capture.read()
    if frame is None:
        break

    frames = frames + 1

    # Get min corners for 10 frames:
    if frames < 10:
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

    # Perspective transform on frame to get table only with right measurements:
    frame = getTableFromFrame(corners, frame)

    # Detect box centers and angles:
    (centers, angles) = detector.Detect(frame)

    # Track box centers:
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

    keyboard = cv.waitKey(1)
    if keyboard == 'q' or keyboard == 27:
        break


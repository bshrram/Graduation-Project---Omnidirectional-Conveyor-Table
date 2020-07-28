import numpy as np
import cv2 as cv

def filterConts(contours):
    newConts = []
    for contour in contours:
        print(contour)
        if len(contour) < 4:
             continue
        area = cv.contourArea(contour)
        if area <= 3500:
            continue
        newConts.append(contour)
    return newConts

def orientations(contours):
    angles = []
    pos = []
    for contour in contours:
        (x, y), (MA, ma), angle = cv.fitEllipse(contour)
        angles.append(angle)
        pos.append((x, y, MA, ma))
    return (angles, pos)

class Detector:
    """Detector class to detect objects in video frame
    Attributes:
        None
    """
    def __init__(self, type, color = None):
        """Initialize variables used by Detectors class
        Args:
            type: detection method: (only COLOR for now)
            color: lower and upper threshold color in HSV
        """
        if type == "COLOR":
            self.type = "COLOR"
            self.color = color

    def Detect(self, frame):
        """Detect objects in video frame
        Args:
            frame: single video frame
        Return:
            (centers: vector of object centroids in a frame,
            angles: vector of angles in a frame)
        """
        if self.type == 'COLOR':
            (lower, upper) = self.color
            hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV) 
            mask = cv.inRange(hsv, lower, upper)
        
        contours, hierarchy = cv.findContours(
            mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        contours_image = np.copy(frame)
        newConts = filterConts(contours)
        
        centers = []  # vector of object centroids in a frame

        # Find centroid for each valid contours
        for cnt in newConts:
            try:
                # Calculate and draw circle
                (x, y), radius = cv.minEnclosingCircle(cnt)
                centeroid = (int(x), int(y))
                radius = int(radius)
                cv.circle(frame, centeroid, radius, (0, 255, 0), 2)
                b = np.array([[x], [y]])
                centers.append(np.round(b))
            except ZeroDivisionError:
                pass

        contours_image = cv.drawContours(
            contours_image, newConts, -1, (0, 255, 0), 3)
        angles = orientations(newConts)
        
        cv.imshow('Frame', contours_image)
        cv.imshow('Mask', mask)
        return (centers, angles)


        

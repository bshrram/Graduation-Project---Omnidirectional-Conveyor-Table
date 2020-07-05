import numpy as np
import cv2 as cv

def newC(contours):
    newConts = []
    for contour in contours:
        if len(contour) < 5:
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
        area = cv.contourArea(contour)
        if area <= 500:  # skip ellipses smaller then 10x10
            continue
        if len(contour) >= 5:
            (x, y), (MA, ma), angle = cv.fitEllipse(contour)
            angles.append(angle)
            pos.append((x, y, MA, ma))
    return (angles, pos)

class Detector:
    def __init__(self, type, color = None):
        if type == "MOG2":
            self.type = "bgs"
            self.fgbg = cv.createBackgroundSubtractorMOG2()
        elif type == "KNN":
            self.type = "bgs"
            self.fgbg = cv.createBackgroundSubtractorKNN()
        elif type == "COLOR":
            self.type = "COLOR"
            self.color = color
        # if self.fgbg:
        #     self.fgbg.setDetectShadows(0)
        #     self.fgbg.setDist2Threshold(800)
        #     self.fgbg.setHistory(1000)
        #     self.fgbg.setkNNSamples(3)
            
            
        #     print (self.fgbg.getShadowThreshold())
        

    def Detect(self, frame, backSub = None):
        if self.type == "bgs":
            if backSub:
                self.fgbg = backSub

            fgMask = self.fgbg.apply(frame)

        if self.type == 'COLOR':
            (lower, upper) = self.color
            hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV) 
            fgMask = cv.inRange(hsv, lower, upper)
            #res = cv.bitwise_and(frame, frame, fgMask=fgMask)
        
        contours, hierarchy = cv.findContours(
            fgMask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        contours_image = np.copy(frame)
        newConts = newC(contours)
        
        centers = []  # vector of object centroids in a frame
        # we only care about centroids with size of bug in this example
        # recommended to be tunned based on expected object size for
        # improved performance
        blob_radius_thresh = 8
        # Find centroid for each valid contours
        for cnt in newConts:
            try:
                # Calculate and draw circle
                (x, y), radius = cv.minEnclosingCircle(cnt)
                centeroid = (int(x), int(y))
                radius = int(radius)
                if (radius > blob_radius_thresh):
                    cv.circle(frame, centeroid, radius, (0, 255, 0), 2)
                    b = np.array([[x], [y]])
                    centers.append(np.round(b))
            except ZeroDivisionError:
                pass

        contours_image = cv.drawContours(
            contours_image, newConts, -1, (0, 255, 0), 3)
        angles = orientations(newConts)
        
        cv.rectangle(contours_image, (10, 2),
                        (100, 20), (255, 255, 255), -1)
        cv.putText(contours_image, str(angles), (15, 15),
                    cv.FONT_HERSHEY_SIMPLEX, 0.3, (0, 0, 0))
        #backgroundImage = self.fgbg.getBackgroundImage()
        #cv.imshow('background', backgroundImage)
        cv.imshow('Frame', contours_image)
        cv.imshow('FG Mask', fgMask)
        return (centers, angles)


        

import numpy as np

def dprint(*args, **kwargs):
    """Debug print function using inbuilt print
    Args:
        args   : variable number of arguments
        kwargs : variable number of keyword argument
    Return:
        None.
    """
    # print(*args, **kwargs)
    pass

def anorm2(a):
    return (a*a).sum(-1)

def anorm(a):
    return np.sqrt( anorm2(a) )

def getsize(img):
    h, w = img.shape[:2]
    return w, h

def pixelToMm(location,w1,h1):
    (x,y)= location
    xm = x * 1150/ w1
    ym = y * 800 / h1
    # print(w1, h1)
    return (xm, ym)

def mmToPixel(location,w1,h1):
    (x,y)= location
    xp = int(x * w1/1150)
    yp =  int(y * h1/800)
    # print(w1, h1)
    return (xp, yp)

import math
def mapping(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return int(rightMin + (valueScaled * rightSpan))


def constrain(val, min_val, max_val):
    return int(min(max_val, max(min_val, val)))

def calculateDistance(l1, l2):
    (x1, y1) = l1
    (x2, y2) = l2
    dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return dist 
    
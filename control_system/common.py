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
    
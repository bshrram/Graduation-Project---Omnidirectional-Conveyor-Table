import math
import pymata_express
import numpy
#import Motor

#motor1 = Motor()
#motor2 = Motor()
#motor3 = Motor()

def translate(value, leftMin, leftMax, rightMin, rightMax):
        # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)
def constrain(val, min_val, max_val):
    return min(max_val, max(min_val, val))

def Move(angle, Magnitude, w):
    theta = angle * 1000 / 57296
    vx = Magnitude * math.cos(theta)
    vy = Magnitude * math.sin(theta)
    w1 = -vx + w
    w2 = 0.5 * vx + (math.sqrt(3) / 2.0) * vy + w
    w3 = 0.5 * vx - (math.sqrt(3) / 2.0) * vy + w
    w1 = constrain(w1, -150, 150)
    w2 = constrain(w2, -150, 150)
    w3 = constrain(w3, -150, 150)
    w1_ccw = w1 < 0 and True or False
    w2_ccw = w2 < 0 and True or False
    w3_ccw = w3 < 0 and True or False
    w1_speed =  translate(abs(w1), 0, 150, 0, 255)
    w2_speed =  translate(abs(w2), 0, 150, 0, 255)
    w3_speed =  translate(abs(w3), 0, 150, 0, 255)
    #motor1.run(w1_ccw,w1_speed)
    #motor2.run(w2_ccw,w2_speed)
    #motor3.run(w3_ccw,w3_speed)
    print(w1_ccw)
    print(w1_speed)
    print(w2_ccw)
    print(w2_speed)
    print(w3_ccw)
    print(w3_speed)
Move(90, 100, 0)
from Master.master import *

class Motor:
    """Motor class that represents motors
    Attributes:
        None
    """

    def __init__(self, motor):
        """Initialize variables used by Motor class
        Args:
            motor: dict represents motor data:
                motor.id: int
                motor.pins: dict:
                    {'digital':tuple, 'pwm': int, 'digMaster': boolean, 'pwmMaster': boolean}
        """
        self.id = motor.id
        self.pins = motor.pins
        self.pinsValues = (0, 0, 0)
    def getStatus(self):
        return (pins, pinsValues)

    def setValues(self, newValues):
        self.pinsValues = newValues

    def run(self, cw, speed):
        self.setValues(cw, not cw, speed)
        

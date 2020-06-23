from Master.master import *

class Motor:
    """Motor class that represents motors
    Attributes:
        None
    """

    def __init__(self, motor):
        """Initialize variables used by Motor class \n
        @Args: \n
            motor: dict represents motor data:
                motor.id: int
                motor.pins: dict:
                    {'digital':tuple, 'pwm': int}
        """
        self.id = motor['id']
        self.pins = motor['pins']
        self.code = motor['code']
        self.pinsValues = (0, 0, 0)

    def getStatus(self):
        return (self.pins, self.pinsValues)

    def setValues(self, newValues):
        self.pinsValues = newValues

    def run(self, cw, speed, control=False):
        newValues = (cw, not cw, speed)
        if control:
            handleMotor(self.pins, self.code, newValues)
        self.setValues(newValues)

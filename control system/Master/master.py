from pymata4 import pymata4

def init_pins():
    pass

def handleMotor(pins, code):  # **** TODO
    """
    handle Motor to control. \n
    Args: \n
        pins: dict
        code: int: 
            1: digital in slave, pwm in master
            2: digital in master, pwm in slave
            3: digital & pwm in slave
            4: digital & pwm in master
    """
    


board = pymata4.Pymata4()
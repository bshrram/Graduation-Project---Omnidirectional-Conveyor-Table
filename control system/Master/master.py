from pymata4 import pymata4

board = pymata4.Pymata4()


def init_pins():
    pass


def handleMotor(pins, code, newValues):  # **** TODO
    """
    handle Motor to control. \n
    Args: \n
        pins: dict
        code: int: 
            1: digital in slave, pwm in master
            2: digital & pwm in slave
            3: digital in master, pwm in slave
            4: digital & pwm in master
    """
    d1, d2 = pins['digital'], pwm = pins['pwm']
    d1v, d2v, pwmv = newValues
    if code == 1:
        board.i2c_write(8, [code, d1, d1v])
    elif code == 2:
        board.i2c_write(8, [code, d1, d1v, pwm, pwmv])   
    elif code == 3:
        board.i2c_write(8, [code,pwm, pwmv])       
    elif code == 4:
        board.digital_write(d1, d1v)
        board.digital_write(d2, d2v)
        board.digital_write(pwm, pwmv)

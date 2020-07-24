from pymata4 import pymata4

#board = pymata4.Pymata4(com_port="COM9")
try:
    board = pymata4.Pymata4()
    board.set_pin_mode_i2c()

    for i in range(2,14):
        board.set_pin_mode_pwm_output(i)

    for i in range(22, 54):
        board.set_pin_mode_digital_output(i)

except:
    pass

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
    d1, d2 = pins['digital'] 
    pwm = pins['pwm']
    d1v, d2v, pwmv = newValues
    # print(("pwm", pwm, pwmv))
    # print(("d1", d1, d1v))
    # print(("d2", d2, d2v))
    
    if code == 1:
        board.i2c_write(8, [code, d1, d1v, d2v])
        board.pwm_write(pwm,pwmv)
    elif code == 2:
        board.i2c_write(8, [code, d1, d1v, d2v, pwm, pwmv])   
    elif code == 3:
        board.i2c_write(8, [code,pwm, pwmv])
        board.digital_write(d1, d1v)
        board.digital_write(d2, d2v)       
    elif code == 4:
        board.digital_write(d1, d1v)
        board.digital_write(d2, d2v)
        board.pwm_write(pwm, pwmv)
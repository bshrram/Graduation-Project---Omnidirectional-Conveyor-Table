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
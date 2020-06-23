import sys, os
from pathlib import Path
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
from table import Table 
cellDatabase = [
    {
        'id': 11,
        'location': [0, 0],
        'code': 1,
        'motors': [
            {'pins': {'digital': (53, 52), 'pwm': 11}},
            {'pins': {'digital': (51, 50), 'pwm': 12}},
            {'pins':{'digital': (49, 48), 'pwm': 13}},
        ]
    }
]

table = Table(cellDatabase)
cell = table.getCellByLocation([0,1])
# print(cell.__dict__)
status = cell.getStatus()
print(status)
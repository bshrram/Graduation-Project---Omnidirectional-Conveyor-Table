from table import Table
import sys
import os
from pathlib import Path
sys.path.append(os.path.join(os.path.dirname(
    os.path.realpath(__file__)), os.pardir))

ids = [
    [11, 81, 32, 52, 13],
    [31, 71, 42, 62, 23],
    [21, 61, 12, 72, 33],
    [44, 51, 22, 82, 43]
]

cellDatabase = [
    # cell_1
    {
        'code': 1,
        'motors': [
            {'pins': {'digital': (53, 52), 'pwm': 11}},
            {'pins': {'digital': (51, 50), 'pwm': 12}},
            {'pins': {'digital': (49, 48), 'pwm': 13}},
        ]
    },
    # cell_8
    {
        'code': 4,
        'motors': [
            {'pins': {'digital': (29, 28), 'pwm': 5}},
            {'pins': {'digital': (31, 30), 'pwm': 6}},
            {'pins': {'digital': (33, 32), 'pwm': 7}},
        ]
    },
    # cell_3
    {
        'code': 2,
        'motors': [
            {'pins': {'digital': (33, 32), 'pwm': 2}},
            {'pins': {'digital': (31, 30), 'pwm': 3}},
            {'pins': {'digital': (29, 28), 'pwm': 4}},
        ]
    },
    # cell_5
    {
        'code': 3,
        'motors': [
            {'pins': {'digital': (53, 52), 'pwm': 8}},
            {'pins': {'digital': (51, 50), 'pwm': 9}},
            {'pins': {'digital': (49, 48), 'pwm': 10}},
        ]
    },
    # cell_1
    {
        'code': 1,
        'motors': [
            {'pins': {'digital': (53, 52), 'pwm': 11}},
            {'pins': {'digital': (51, 50), 'pwm': 12}},
            {'pins': {'digital': (49, 48), 'pwm': 13}},
        ]
    },
    # cell_3
    {
        'code': 2,
        'motors': [
            {'pins': {'digital': (33, 32), 'pwm': 2}},
            {'pins': {'digital': (31, 30), 'pwm': 3}},
            {'pins': {'digital': (29, 28), 'pwm': 4}},
        ]
    },
    # cell_7
    {
        'code': 4,
        'motors': [
            {'pins': {'digital': (23, 22), 'pwm': 4}},
            {'pins': {'digital': (25, 24), 'pwm': 3}},
            {'pins': {'digital': (27, 26), 'pwm': 2}},
        ]
    },
    # cell_4
    {
        'code': 2,
        'motors': [
            {'pins': {'digital': (27, 26), 'pwm': 5}},
            {'pins': {'digital': (25, 24), 'pwm': 6}},
            {'pins': {'digital': (23, 22), 'pwm': 7}},
        ]
    },
    # cell_6
    {
        'code': 3,
        'motors': [
            {'pins': {'digital': (47, 38), 'pwm': 11}},
            {'pins': {'digital': (37, 36), 'pwm': 12}},
            {'pins': {'digital': (35, 34), 'pwm': 13}},
        ]
    },
    # cell_2
    {
        'code': 1,
        'motors': [
            {'pins': {'digital': (47, 38), 'pwm': 10}},
            {'pins': {'digital': (37, 36), 'pwm': 9}},
            {'pins': {'digital': (35, 34), 'pwm': 8}},

        ]
    },
    # cell_2
    {
        'code': 1,
        'motors': [
            {'pins': {'digital': (47, 38), 'pwm': 10}},
            {'pins': {'digital': (37, 36), 'pwm': 9}},
            {'pins': {'digital': (35, 34), 'pwm': 8}},

        ]
    },
    # cell_6
    {
        'code': 3,
        'motors': [
            {'pins': {'digital': (47, 38), 'pwm': 11}},
            {'pins': {'digital': (37, 36), 'pwm': 12}},
            {'pins': {'digital': (35, 34), 'pwm': 13}},
        ]
    },
    # cell_1
    {
        'code': 1,
        'motors': [
            {'pins': {'digital': (53, 52), 'pwm': 11}},
            {'pins': {'digital': (51, 50), 'pwm': 12}},
            {'pins': {'digital': (49, 48), 'pwm': 13}},
        ]
    },
    # cell_7
    {
        'code': 4,
        'motors': [
            {'pins': {'digital': (23, 22), 'pwm': 4}},
            {'pins': {'digital': (25, 24), 'pwm': 3}},
            {'pins': {'digital': (27, 26), 'pwm': 2}},
        ]
    },
    # cell_3
    {
        'code': 2,
        'motors': [
            {'pins': {'digital': (33, 32), 'pwm': 2}},
            {'pins': {'digital': (31, 30), 'pwm': 3}},
            {'pins': {'digital': (29, 28), 'pwm': 4}},
        ]
    },
    # cell_4
    {
        'code': 2,
        'motors': [
            {'pins': {'digital': (27, 26), 'pwm': 5}},
            {'pins': {'digital': (25, 24), 'pwm': 6}},
            {'pins': {'digital': (23, 22), 'pwm': 7}},
        ]
    },
    # cell_5
    {
        'code': 3,
        'motors': [
            {'pins': {'digital': (53, 52), 'pwm': 8}},
            {'pins': {'digital': (51, 50), 'pwm': 9}},
            {'pins': {'digital': (49, 48), 'pwm': 10}},
        ]
    },
    # cell_2
    {
        'code': 1,
        'motors': [
            {'pins': {'digital': (47, 38), 'pwm': 10}},
            {'pins': {'digital': (37, 36), 'pwm': 9}},
            {'pins': {'digital': (35, 34), 'pwm': 8}},

        ]
    },
    # cell_8
    {
        'code': 4,
        'motors': [
            {'pins': {'digital': (29, 28), 'pwm': 5}},
            {'pins': {'digital': (31, 30), 'pwm': 6}},
            {'pins': {'digital': (33, 32), 'pwm': 7}},
        ]
    },
    # cell_4
    {
        'code': 2,
        'motors': [
            {'pins': {'digital': (27, 26), 'pwm': 5}},
            {'pins': {'digital': (25, 24), 'pwm': 6}},
            {'pins': {'digital': (23, 22), 'pwm': 7}},
        ]
    },
]
k = 0
for i in range(5):
    for j in range(4):
        cellDatabase[k]['id'] = ids[i][j]
        cellDatabase[k]['location'] = [i, j]
        k += 1

table = Table(cellDatabase)
cell = table.getCellByLocation([0, 1])
# print(cell.__dict__)
status = cell.getStatus()
print(status)

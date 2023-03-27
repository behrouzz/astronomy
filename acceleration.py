"""
Acceleration of an object on earth surface due to earth rotation
"""

import numpy as np


re = 6378.1366 * 1000 # equatorial radius
T = 86164.098903691 # period (1 stellar day)

v = (2 * np.pi * re) / T
print('Speed:', v)

a = v**2 / re
print('Acceleration:', a)

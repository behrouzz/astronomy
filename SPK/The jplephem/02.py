import numpy as np
from jplephem.spk import SPK

kernel = SPK.open('../bsp_files/de421.bsp')
#print(kernel)

# tell NumPy to make vector output attractive
np.set_printoptions(precision=3)

"""
Each segment of the file lets you predict the position of an object with
respect to some other reference point.

If you want the coordinates of Mars at 2457061.5 (2015 February 8) with
respect to the center of the solar system :
"""

position = kernel[0,4].compute(2457061.5)
print(position)

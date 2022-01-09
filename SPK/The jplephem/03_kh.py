import numpy as np
from jplephem.spk import SPK

kernel = SPK.open('../bsp_files/de421.bsp')

"""
But learning the position of Mars with respect to the Earth takes three steps,
from Mars to the Solar System barycenter to the Earth-Moon barycenter and
finally to Earth itself:
"""

position = kernel[0,4].compute(2457061.5)
position -= kernel[0,3].compute(2457061.5)
position -= kernel[3,399].compute(2457061.5)
print(position)


# khodam
mars = kernel[0,4].compute(2457061.5)
emb  = kernel[0,3].compute(2457061.5)

emb_mars = mars - emb

emb_earth = kernel[3,399].compute(2457061.5)

earth_mars = emb_mars - emb_earth
print(earth_mars)


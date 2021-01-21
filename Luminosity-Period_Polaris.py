"""
Luminosity-Period relation (page 171 pdf)
==========================
We want to calculate the relation between luminosity and period of Polaris,
which is the nearest Cepheid variable star.

In order to calculate the luminosity of Polaris (L), we should first find
it's flux. 

Relation between apparent magnitude (m) and flux (f):

m1 - m2 = -2.5 * np.log10(f1/f2)

if we take Sun as the first object (m1=m_sun, f1=f_sun), the flux of any
object with known apparent magnitude (m) is:

f = f_sun / 10**((m - m_sun)/2.5)
"""

import numpy as np
from astropy import units as u
from astropy.constants import L_sun, au

#-----------------------------------------------
# Known parameters:
# -----------------
m = 2.02 # apparent magnitude of Polaris
plx = 7.54 * u.Unit('mas') # parallax of Polaris (milliarcseconds)
period = 3.97 # period of Polaris (days)
m_sun = -27 # apparent magnitude of Sun
#-----------------------------------------------

# Convert parallax to ArcSecond
plx = plx.to('arcsec')

#  Polaris distance (in pc and converting to m)
d = 1 / plx
d = (d.value * u.Unit('pc')).to('m')

# Polaris flux
f_sun = L_sun / (4 * np.pi * (au**2))
f = f_sun / 10**((m - m_sun)/2.5)

# Polaris luminosity
L = 4 * np.pi * (d**2) * f

# Luminosity-Period relation
print('Luminosity / period =', L / period)

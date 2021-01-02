"""
Calculating Sun's position with two libraries
---------------------------------------------
We want to get the position of the Sun at a certain time with two libraries:
skyfield and astropy.
skyfield will automatically download 'de421.bsp' from its repo and save it
in your working directory.

By: Behrouz Safari
"""

from datetime import datetime
from pytz import timezone

t = datetime(2010, 1, 1, 0, 0, tzinfo=timezone('utc'))

# with skyfield
# =============
from skyfield.api import load

ts = load.timescale()
eph = load('de421.bsp')
t1 = ts.from_datetime(t)
pla = eph['sun'].at(t1)
sun1 = pla.position.km / 1_000_000
print(sun1)

# with astropy
# ============
from astropy.coordinates import get_sun
from astropy.time import Time

t2 = Time(t)
sun2 = get_sun(t2).icrs.cartesian.xyz.to('km') / 1_000_000
print(sun2)

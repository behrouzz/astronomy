import numpy as np
from datetime import datetime, timedelta
import hypatie as hp
from astropy.time import Time

t1 = datetime(2021, 3, 18)
t2 = datetime(2021, 3, 22)
step = 100
delta = (t2-t1).total_seconds() / step

while delta > 0.5:
    d, p = hp.get_position('obs', 'sun', t1, t2, step=step)
    dec = p[:, 1]
    ind = np.argmin(np.abs(dec))
    t1 = d[ind-1]
    t2 = d[ind+1]
    delta = (t2-t1).total_seconds() / step


print('TDB scale => GMT  :', d[ind])
print('TDB scale => IRAN :', d[ind] + timedelta(hours=3.5))
print()
# Converting TDB to UTC
ut = Time(d[ind], scale='tdb').utc
ir = Time(d[ind] + timedelta(hours=3.5), scale='tdb').utc

print('UTC scale => GMT  :', ut)
print('UTC scale => IRAN :', ir)

"""
TDB scale => GMT  : 2021-03-20 09:37:11.885000
TDB scale => IRAN : 2021-03-20 13:07:11.885000

UTC scale => GMT  : 2021-03-20 09:36:02.699380
UTC scale => IRAN : 2021-03-20 13:06:02.699381
"""

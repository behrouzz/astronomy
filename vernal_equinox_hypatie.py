import numpy as np
from datetime import datetime, timedelta
import hypatie as hp

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

print('GMT  :', d[ind])
print('IRAN :', d[ind] + timedelta(hours=3.5))

#GMT  : 2021-03-20 09:37:11.885000
#IRAN : 2021-03-20 13:07:11.885000

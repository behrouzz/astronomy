import numpy as np
from datetime import datetime, timedelta
import hypatie as hp

t1 = datetime(2021, 3, 18)
t2 = datetime(2021, 3, 22)
step = 100
delta = (t2-t1).total_seconds() / step

while delta > 0.5:
    obs = hp.Observer('sun', t1, t2, step=step, center='500@399')
    ind = np.argmin(np.abs(obs.dec))
    t1 = obs.time[ind-1]
    t2 = obs.time[ind+1]
    delta = (t2-t1).total_seconds() / step

print('UTC  :', obs.time[ind])
print('IRAN :', obs.time[ind] + timedelta(hours=3.5))

#UTC  : 2021-03-20 09:37:11.760000
#IRAN : 2021-03-20 13:07:11.760000

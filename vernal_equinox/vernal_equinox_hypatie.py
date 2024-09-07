import numpy as np
from datetime import datetime, timedelta
import hypatie as hp

t1 = datetime(2000, 3, 18)
t2 = datetime(2000, 3, 22)
step = 1000
delta = (t2-t1).total_seconds() / step

while delta > 0.5:
    obs = hp.Observer('sun', t1, t2, step=step, center='500@399')
    ind = np.argmin(np.abs(obs.dec))
    t1 = obs.time[ind-1]
    t2 = obs.time[ind+1]
    delta = (t2-t1).total_seconds() / step


x = obs.dec
y = np.array([i.timestamp() for i in obs.time])
t_ = np.interp(0, x, y)
t = datetime.fromtimestamp(t_)

print('UTC  :', t)
print('IRAN :', t + timedelta(hours=3.5))

#UTC  : 2000-03-20 07:35:00.786376
#IRAN : 2000-03-20 11:05:00.786376

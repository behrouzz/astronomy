import erfa
from datetime import datetime, timedelta
import numpy as np

##def __interpolate(x1, y1, x2, y2, x):
##        a = (y2-y1) / (x2-x1)
##        b = y1 - a*x1
##        return a*x + b
##
##def interpolate(rng, decs):
##    ind = np.argmin(np.abs(decs))
##    dec1 = decs[ind-1]
##    dec2 = decs[ind+1]
##    t1 = rng[ind-1].timestamp()
##    t2 = rng[ind+1].timestamp()
##    t = __interpolate(dec1, t1, dec2, t2, 0)
##    t_vernal = datetime.fromtimestamp(t)
##    return t_vernal

def create_range(t1, t2, steps):
    rng = t2 - t1
    dt = rng / steps
    return [t1 + dt*i for i in range(steps+1)]

def get_tt(t):
    utc1, utc2 = erfa.dtf2d('UTC', t.year, t.month, t.day, t.hour, t.minute, t.second + (t.microsecond / 1e6))
    tai1, tai2 = erfa.utctai(utc1, utc2)
    tt1, tt2 = erfa.taitt(tai1, tai2)
    return tt1, tt2


t1 = datetime(2024, 3, 19)
t2 = datetime(2024, 3, 21)
rng = create_range(t1, t2, 1000)

decs = np.zeros((len(rng),))

for i, t in enumerate(rng):
    tt1, tt2 = get_tt(t)
    astrom, eo = erfa.apci13(tt1, tt2)
    sunGCRS = -astrom[2]*astrom[3]
    raG, decG, _ = erfa.p2s(sunGCRS)
    _, decs[i] = erfa.atciqz(raG, decG, astrom)

##t = interpolate(rng, decs)

x = decs
y = np.array([i.timestamp() for i in rng])
t_ = np.interp(0, x, y)
t = datetime.fromtimestamp(t_)


print('UTC   :', t)
print('Tehran:', t + timedelta(hours=3.5))

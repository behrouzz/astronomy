import erfa
from datetime import datetime, timedelta
import numpy as np


def create_range(t1, t2, steps):
    rng = t2 - t1
    dt = rng / steps
    return [t1 + dt*i for i in range(steps+1)]

def get_tt(t):
    utc1, utc2 = erfa.dtf2d('UTC', t.year, t.month, t.day, t.hour, t.minute, t.second + (t.microsecond / 1e6))
    tai1, tai2 = erfa.utctai(utc1, utc2)
    tt1, tt2 = erfa.taitt(tai1, tai2)
    return tt1, tt2


t1 = datetime(2024, 3, 20, 3, 0)
t2 = datetime(2024, 3, 20, 3, 10)
rng = create_range(t1, t2, 10000)

gcrs = np.zeros((len(rng),3))
cirs = np.zeros((len(rng),3))

for i, t in enumerate(rng):
    tt1, tt2 = get_tt(t)
    
    astrom, eo = erfa.apci13(tt1, tt2)

    sunGCRS = -astrom[2]*astrom[3]
    rag, decg, rg = erfa.p2s(sunGCRS)
    gcrs[i][0] = np.degrees(rag)
    gcrs[i][1] = np.degrees(decg)
    gcrs[i][2] = rg

    r, d = erfa.atciqz(rag, decg, astrom)
    cirs[i][0] = np.degrees(r)
    cirs[i][1] = np.degrees(d)
    cirs[i][2] = rg


ind1 = np.argmin(np.abs(gcrs[:,1]))
print('GCRS       :', rng[ind1], '(Not Acceptable)')
ind = np.argmin(np.abs(cirs[:,1]))
print('CIRS (UTC) :', rng[ind])

print('CIRS (Iran):', rng[ind] + timedelta(hours=3.5))

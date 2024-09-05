import erfa
from iers import EOP
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt


def create_range(t1, t2, steps):
    rng = t2 - t1
    dt = rng / steps
    return [t1 + dt*i for i in range(steps+1)]

def get_time(t):
    utc1, utc2 = erfa.dtf2d('UTC', t.year, t.month, t.day, t.hour, t.minute, t.second + (t.microsecond / 1e6))
    tai1, tai2 = erfa.utctai(utc1, utc2)
    tt1, tt2 = erfa.taitt(tai1, tai2)
    return utc1, utc2, tt1, tt2


t = datetime.utcnow()

t1 = datetime(1982, 1, 1)
t2 = datetime(2025, 1, 1)
steps = 100
rng = create_range(t1, t2, steps)

ra = np.zeros((len(rng),))
dec = np.zeros((len(rng),))

for i, t in enumerate(rng):
    utc1, utc2, tt1, tt2 = get_time(t)
    r = erfa.pnm06a(tt1, tt2)
    ra[i], dec[i] = erfa.c2s(r[-1, :])


ra = erfa.anp(ra)

fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
ax.scatter(ra*erfa.DR2D, 90-(dec*erfa.DR2D), s=1)


for i in [*range(0, steps, 5)]+[-1]:
    ax.text(ra[i]*erfa.DR2D, 90-(dec[i]* erfa.DR2D),
            s=rng[i].isoformat()[:4],
            fontsize='small', rotation=0, alpha=0.5)

plt.show()

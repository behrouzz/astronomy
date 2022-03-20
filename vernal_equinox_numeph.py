from numeph import load_txt
from datetime import datetime, timedelta
from hypatie.transform import to_tete
from hypatie.time import utc2tdb, tdb2utc
from hypatie import mag
import numpy as np


def create_range(t1, t2, steps):
    rng = t2 - t1
    dt = rng / steps
    return [t1 + dt*i for i in range(steps+1)]

def get_range(tw, last=False):
    tw = [utc2tdb(i) for i in tw]
    ts = []
    decs = []
    dts = []
    for t in tw:
        earB_ear = dc[(3,399)].get_pos(t)
        SSB_plaB = dc[(0, 10)].get_pos(t)
        SSB_earB = dc[(0, 3)].get_pos(t)
        pos = SSB_plaB - earB_ear - SSB_earB
        pos_tete = to_tete(pos, t)
        distance = mag(pos_tete)
        dt = distance / 299792.458
        dts.append(dt)
        time = tdb2utc(t)+timedelta(seconds=dt)
        ts.append(time)
        decs.append(pos_tete[-1])

    ind = np.argmin(np.abs(np.array(decs)))

    t1 = tdb2utc(tw[ind-1])
    t2 = tdb2utc(tw[ind+1])

    if last:
        t1 = t1+timedelta(seconds=dts[ind-1])
        t2 = t2+timedelta(seconds=dts[ind+1])
    return t1, t2


dc = load_txt('de440_2022-03-20.txt')

t1 = datetime(2022, 3, 20, 1)
t2 = datetime(2022, 3, 20, 23)
steps = 5

while abs((t2-t1).total_seconds()) > 0.01:
    tw = create_range(t1, t2, steps)
    t1, t2 = get_range(tw)

tw = create_range(t1, t2, steps)
t1, t2 = get_range(tw, last=True)

print(t1 + (t2-t1)/2)

"""
2022-03-20 15:33:23.687276
"""


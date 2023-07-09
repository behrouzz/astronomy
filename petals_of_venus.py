import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import spiceypy as sp
from hypatie.animation import Body, play2d, play

AU = 149597870.7 #km

adr = 'C:/Users/H21/Desktop/Desktop/Behrouz/Astronomy/kernels/'
kernels = [adr+'de440s.bsp', adr+'naif0012.tls']

t0 = datetime.utcnow()
ts = [t0 + timedelta(days=i) for i in range(int(8*365))]

for k in kernels:
    sp.furnsh(k)


pos_sun = []
pos_ven = []

for t in ts:
    et = sp.str2et(str(t))
    state, _ = sp.spkez(targ=2, et=et, ref='J2000', abcorr='NONE', obs=399)
    pos_ven.append(state[:3])
    state, _ = sp.spkez(targ=10, et=et, ref='J2000', abcorr='NONE', obs=399)
    pos_sun.append(state[:3])
pos_ven = np.array(pos_ven)/AU
pos_sun = np.array(pos_sun)/AU


sp.kclear()

sun = Body('Sun', pos_sun, ts)
venus = Body('Venus', pos_ven, ts)
earth = Body('Earth', np.zeros(pos_sun.shape), ts)


anim = play2d(bodies=[sun, earth, venus],
              names=['Sun', 'Earth', 'Venus'],
              colors=['y', 'b', 'g'],
              sizes=[10, 20, 2],
              path=True,
              title='Pentagram (petals) of Venus')

plt.show()

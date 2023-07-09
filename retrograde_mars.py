import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import spiceypy as sp
from hypatie.animation import Body, play2d, play
from hypatie.transform import equ_car2ecl_car

AU = 149597870.7 #km

adr = 'C:/Users/H21/Desktop/Desktop/Behrouz/Astronomy/kernels/'
kernels = [adr+'de440s.bsp', adr+'naif0012.tls']

t0 = datetime.utcnow()
ts = [t0 + timedelta(days=i) for i in range(int(79.06*365))]

for k in kernels:
    sp.furnsh(k)


pos_sun = []
pos_mar = []

for t in ts:
    et = sp.str2et(str(t))
    state, _ = sp.spkez(targ=4, et=et, ref='J2000', abcorr='NONE', obs=399)
    pos_mar.append(state[:3])
    state, _ = sp.spkez(targ=10, et=et, ref='J2000', abcorr='NONE', obs=399)
    pos_sun.append(state[:3])

pos_mar = [equ_car2ecl_car(i) for i in pos_mar]
pos_sun = [equ_car2ecl_car(i) for i in pos_sun]
pos_mar = np.array(pos_mar)/AU
pos_sun = np.array(pos_sun)/AU


sp.kclear()

sun = Body('Sun', pos_sun, ts)
mars = Body('Mars', pos_mar, ts)
earth = Body('Earth', np.zeros(pos_sun.shape), ts)


anim = play2d(bodies=[sun, earth, mars],
              names=['Sun', 'Earth', 'Mars'],
              colors=['y', 'b', 'k'],
              sizes=[10, 20, 2],
              path=True,
              title='Retrograde motion of Mars around the Earth',
              interval=1)

plt.show()

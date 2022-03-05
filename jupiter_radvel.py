from datetime import datetime, timedelta
from numeph import SPK, load_pickle
import pickle
import numpy as np

adr = 'C:/Users/H21/Desktop/Desktop/Behrouz/Astronomy/SPK/bsp_files/'
#adr = 'https://naif.jpl.nasa.gov/pub/naif/pds/wgc/kernels/spk/'


t1 = datetime(2021, 1, 1)
t2 = datetime(2022,1, 1)

# jupiter
jup_tup = [(5, 501), (5, 502), (5, 503), (5, 504), (5, 599)]
jup = SPK(fname=adr+'jup310.bsp', t1=t1, t2=t2, segs_tup=jup_tup)

# solar system
sol_tup = [(0, 5), (0, 3), (3, 399), (0, 10)]
sol = SPK(fname=adr+'de440.bsp', t1=t1, t2=t2, segs_tup=sol_tup)

dc = {**sol.array, **jup.array}

with open('jup.pickle', 'wb') as f:
    pickle.dump(dc, f)

#=====================================================
# geocentric position of jupiter barycenter
# ----------------------------------------------------
segs = load_pickle('jup.pickle')

def geo_jup(segs, t):
    p3_399 = segs[(3,399)].get_pos(t)
    p0_5   = segs[(0,  5)].get_pos(t)
    p0_3   = segs[(0,  3)].get_pos(t)


    p399_5 = p0_5 - p3_399 - p0_3
    return p399_5

dt = (t2-t1).days
t = [t1 + timedelta(days=i) for i in range(dt)]

pos = np.array([geo_jup(segs, i) for i in t])

#=====================================================
# Radial velocity of Jupiter wrt Earth
# ----------------------------------------------------

import matplotlib.pyplot as plt

def mag(x):
    return np.linalg.norm(np.array(x))

def unit(x):
    return x / mag(x)

vel = np.zeros((len(pos)-1, 3))

for i in range(len(pos)-1):
    vel[i, :] = pos[i+1]-pos[i]


# projection of vector vel on vector (unit) pos
prj_vel = np.zeros(vel.shape)

# unit vector of position
pos_u = np.array([unit(i) for i in pos[1:]])

radvel = np.zeros(pos_u.shape[0])
for i in range(len(pos_u)):
    v = vel[i]
    w = pos_u[i]
    a = np.dot(v,w) / mag(w)**2
    #prj_vel[i, :] = a * w
    radvel[i] = a

i_max = np.argmax(radvel)
i_min = np.argmin(radvel)

print('Moving away :', t[1:][i_max], ':', radvel[i_max])
print('Approching  :', t[1:][i_min], ':', radvel[i_min])

plt.plot(t[1:], radvel)
plt.grid()
plt.show()

#=====================================================
# Animation
# ----------------------------------------------------

from hypatie.animation import Body, play

ear_pos = np.array([segs[(0,3)].get_pos(i) for i in t])
jup_pos = np.array([segs[(0,5)].get_pos(i) for i in t])
sun_pos = np.zeros(ear_pos.shape)

sun = Body('Sun', sun_pos, t)
earth = Body('Earth', ear_pos, t)
jupiter = Body('Jupiter', jup_pos, t)

bodies = [sun, earth, jupiter]
names = ['Sun', 'Earth', 'Jupiter']
colors = ['y', 'b','r']
sizes = [20, 5, 8]

anim = play(bodies, names, colors, sizes)
plt.show()

"""
Janus and Epimetheus orbits in rotating reference frame
Using hypatie python package
"""

import pickle
import hypatie as hp
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def smooth(pos, n):
    df = pd.DataFrame(pos)
    df = df.rolling(n).mean()[n:]
    return df.values

t1 = '2008-01-01 12:00:00'
t2 = '2018-01-01 12:00:00'

# Get coordinates from Horizons (center: barycenter of saturn system)
janus = hp.Vector('610', t1, t2, center='500@6', step=500)
epimetheus  = hp.Vector('611', t1, t2, center='500@6', step=500)

time = janus.time

# Convert coordinates to xy plane (z=0)
plane_pos_jan = hp.to_xy_plane(janus.pos)
plane_pos_epi = hp.to_xy_plane(epimetheus.pos)

jan_period = 0.694660342
epi_period = 0.694333517 # not used

# Convert coordinates to rotating reference frame (rotate around z axis)
rot_pos_jan = hp.rotating_coords(plane_pos_jan, jan_period, time)
rot_pos_epi = hp.rotating_coords(plane_pos_epi, jan_period, time)

smth = 20
jan = hp.Body('Janus', smooth(rot_pos_jan, smth), time[smth:])
epi = hp.Body('Epimetheus', smooth(rot_pos_epi, smth), time[smth:])
sat = hp.Body('Saturn', np.zeros(jan.pos.shape), time[smth:])

bodies = [sat, jan, epi]
names = [i.name for i in bodies]
colors = ['b', 'r', 'g']
sizes = [30, 10, 8]

title = 'Janus & Epimetheus orbits in rotating frame with '+r'$\omega=9$'+' rad/day'
title = title + '\nhttps://github.com/behrouzz/hypatie'

anim = hp.play2d(bodies, names, colors, sizes, interval=15,
                 repeat=False, title=title)
plt.show()
#anim.save('jan_epi.mp4')

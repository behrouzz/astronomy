import numpy as np
from hypatie import mag
from bspice import lonlat_to_cartesian



def centrifugal_force(obs_loc, m):
    om = (2*np.pi) / 86164.09053083288
    x, y, z = lonlat_to_cartesian(obs_loc)
    r = np.sqrt(x**2 + y**2) * 1000
    F = m * (om**2) * r
    return F


def real_g(obs_loc):
    G = 6.6743e-11 # m3 / (kg s2)
    M = 5.972167867791379e+24 # mass of Earth (kg)
    r = mag(lonlat_to_cartesian(obs_loc)) * 1000
    g = (G*M)/(r**2)
    return g



m = 100

dc = {'pol': (0, 90, 0), 'equ':(0, 0, 0)}

for k,v in dc.items():
    print(k)
    obs_loc = v
    
    g = real_g(obs_loc)
    W = m * g
    F_cent = centrifugal_force(obs_loc, m)
    print('W      :', W)
    print('F_cent :', F_cent)
    print('F_total:', W - F_cent)
    print('-'*70)

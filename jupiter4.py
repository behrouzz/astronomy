"""
from datetime import datetime
from numeph import SPK

t1 = datetime(2020, 1, 1)
t2 = datetime(2030, 1, 1)


adr = "C:/Users/H21/Desktop/Desktop/Behrouz/Astronomy/SPK/bsp_files/"
file = adr + 'jup310.bsp'

segs_tup = [(5, 501), (5, 502), (5, 503), (5, 504), (5, 599),
            (0, 3), (0, 5), (3, 399)]

spk = SPK(fname=file, segs_tup=segs_tup, t1=t1, t2=t2)

spk.to_pickle('jup4_2020_2030.pickle')
"""


from datetime import datetime
from hypatie.solar_system import load_pickle
from hypatie.time import utc2tdb
import matplotlib.pyplot as plt
import numpy as np


diam = {0:139820, 1:3643.2, 2:3121.6, 3:5268.2, 4:4820.6}


def ang_diam(diam, dist):
    """angular diameter in arcsec"""
    return 206265 * (diam/dist)


def jupiter_moons(dc, t, gcrs=False):
        
    tdb = utc2tdb(t)
    
    if gcrs:
        earth = dc[(0, 3)].get_pos(tdb) + dc[(3, 399)].get_pos(tdb)
    else:
        earth = np.array([0,0,0])

    jup0 = dc[(0, 5)].get_pos(tdb) + dc[(5, 599)].get_pos(tdb) - earth
    jup1 = dc[(0, 5)].get_pos(tdb) + dc[(5, 501)].get_pos(tdb) - earth
    jup2 = dc[(0, 5)].get_pos(tdb) + dc[(5, 502)].get_pos(tdb) - earth
    jup3 = dc[(0, 5)].get_pos(tdb) + dc[(5, 503)].get_pos(tdb) - earth
    jup4 = dc[(0, 5)].get_pos(tdb) + dc[(5, 504)].get_pos(tdb) - earth

    coords = [jup0, jup1, jup2, jup3, jup4]

    return coords


adr = 'https://github.com/behrouzz/astrodatascience/raw/main/spk/'


dc = load_pickle(adr+'jup310_2020_2030.pickle')

t = datetime.utcnow()

coords = jupiter_moons(dc, t, gcrs=False)

jup0, jup1, jup2, jup3, jup4 = coords


##fig, ax = plt.subplots()
##ax.scatter([jup0[0]], [jup0[1]], s=100, c='r')
##ax.scatter([jup1[0]], [jup1[1]], c='k')
##ax.scatter([jup2[0]], [jup2[1]], c='b')
##ax.scatter([jup3[0]], [jup3[1]], c='g')
##ax.scatter([jup4[0]], [jup4[1]], c='orange')
##plt.show()

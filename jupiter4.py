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

spk.to_pickle('jup310_2020_2030.pickle')
"""

from datetime import datetime
from hypatie.solar_system import load_pickle
from hypatie.time import utc2tdb
import matplotlib.pyplot as plt
import numpy as np
from astropy.coordinates import SkyCoord, EarthLocation, AltAz
from astropy.time import Time



diam = {0:139820, 1:3643.2, 2:3121.6, 3:5268.2, 4:4820.6}


def angular_diameter(diam, dist):
    """angular diameter in arcsec"""
    return 206265 * (diam/dist)


def jupiter_moons(dc, t, frame='icrs', location=None):
        
    tdb = utc2tdb(t)
    
    if frame=='icrs':
        earth = np.array([0,0,0])
    else:
        earth = dc[(0, 3)].get_pos(tdb) + dc[(3, 399)].get_pos(tdb)
        
    jup0 = dc[(0, 5)].get_pos(tdb) + dc[(5, 599)].get_pos(tdb) - earth
    jup1 = dc[(0, 5)].get_pos(tdb) + dc[(5, 501)].get_pos(tdb) - earth
    jup2 = dc[(0, 5)].get_pos(tdb) + dc[(5, 502)].get_pos(tdb) - earth
    jup3 = dc[(0, 5)].get_pos(tdb) + dc[(5, 503)].get_pos(tdb) - earth
    jup4 = dc[(0, 5)].get_pos(tdb) + dc[(5, 504)].get_pos(tdb) - earth

    X = [jup0[0], jup1[0], jup2[0], jup3[0], jup4[0]]
    Y = [jup0[1], jup1[1], jup2[1], jup3[1], jup4[1]]
    Z = [jup0[2], jup1[2], jup2[2], jup3[2], jup4[2]]

    if (frame=='altaz') and (location is not None):
        lon, lat = location
        loc = EarthLocation(lon=lon, lat=lat)
        T = Time(tdb, scale='tdb')
        altaz = AltAz(obstime=T, location=loc)
        c = SkyCoord(x=X, y=Y, z=Z, unit='km', representation_type='cartesian')
        coords = c.transform_to(altaz)
    else:
        coords = [jup0, jup1, jup2, jup3, jup4]

    return coords


adr = 'https://github.com/behrouzz/astrodatascience/raw/main/spk/'
adr = ''

dc = load_pickle(adr+'jup310_2020_2030.pickle')

t = datetime.utcnow()

names = ["Jupiter", "IO", "Europa", "Ganymede", "Callisto"]
colors = ['r', 'k', 'b', 'g', 'orange']

# GCRS coords
c = jupiter_moons(dc, t, frame='altaz', location=(7, 45))


distance = c.distance.value
ang_diam = np.array([angular_diameter(diam[i], distance[i]) for i in range(5)])


n = 20
sizes = (ang_diam*n).round()

fig, ax = plt.subplots()
ax.scatter(c.az.value, c.alt.value, s=sizes, c=colors)
for i, label in enumerate(names):
    plt.text(c.az.value[i], c.alt.value[i], label)
plt.grid()
plt.xlabel('Az')
plt.ylabel('Alt')
plt.show()

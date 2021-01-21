"""
Plot brilliant stars in ICRS frame
"""

import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from astropy.time import Time
from astropy import units as u
from astropy.coordinates import SkyCoord, EarthLocation, AltAz

# Maximum apparent magnitude
x = 3

sql = f"""SELECT TOP 10000 oid, ra, dec, allfluxes.V FROM basic
JOIN allfluxes ON basic.oid=allfluxes.oidref
WHERE allfluxes.V < {x}"""
sql = sql.replace('\n', ' ')
base = 'http://simbad.u-strasbg.fr/simbad/sim-tap/sync?'
base = base + 'request=doQuery&lang=adql&format=json&query='
r = requests.get(base+sql).json()
meta = pd.DataFrame(r['metadata'])
cols = [i['name'] for i in r['metadata']]
df = pd.DataFrame(r['data'], columns=cols)

ra = df['ra'].values * u.degree
dec = df['dec'].values * u.degree

c = SkyCoord(ra=ra, dec=dec, frame='icrs')

ra_rad = c.ra.wrap_at(180 * u.deg).radian
dec_rad = c.dec.radian

m = df['V'].values

plt.figure(figsize=(8,4.2))
plt.subplot(111, projection="aitoff")
plt.title(f"Stars with magnitude less than {x} (frame: ICRS)", y=1.08)
plt.grid(True)
for i in range(len(m)):
    plt.plot(ra_rad[i], dec_rad[i], 'o', markersize=x-m[i], c='k')
# Use markersize=(x-m[i])*x for more distinction
plt.subplots_adjust(top=0.95,bottom=0.0)
plt.show()

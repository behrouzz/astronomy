# Number of points on Earth: 312
# Number of time moments: 96 (each 15 min in one day)

import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from astropy import units as u
from astropy.time import Time
from astropy.coordinates import EarthLocation, Longitude, Latitude
from hypatie.animation import Body, play

t0 = datetime(2022,1,1,0,0,0)
times = [t0 + 0.25*timedelta(hours=i) for i in range(96)]
ts = Time(times)

lats = np.array([*range(-90, 105, 15)])
lons = np.array([*range(-180, 180, 15)])

crd = []
for y in lats:
    for x in lons:
        crd.append(np.array([y,x]))

crd = np.array(crd)

n = [str(i).zfill(3) for i in range(len(crd))]

lats = crd[:,0]
lons = crd[:,1]

lons = lons * u.Unit('deg')
lats = lats * u.Unit('deg')

lons = Longitude(lons)
lats = Latitude(lats)

locs = EarthLocation.from_geodetic(lon=lons, lat=lats)

pos = np.array([locs.get_gcrs(i).cartesian.xyz.value for i in ts])
print(pos.shape)

bodies = [Body(n[i], pos[:,:,i], times) for i in range(len(locs))]
names = n
colors = ['blue']*len(locs)
sizes = [1]*len(locs)

anim = play(bodies, names, colors, sizes, legend=False, path=False)
plt.show()

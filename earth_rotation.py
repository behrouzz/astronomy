# Number of points on Earth: n=300
# Number of time moments: 96 (each 15 min in one day)

import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from astropy import units as u
from astropy.time import Time
from astropy.coordinates import EarthLocation, Longitude, Latitude
from hypatie.animation import Body, play

n = 300
t0 = datetime(2022,1,1,0,0,0)
times = [t0 + 0.25*timedelta(hours=i) for i in range(96)]
ts = Time(times)

# Choose random points on the surface of a sphere
# https://mathworld.wolfram.com/SpherePointPicking.html
rand1, rand2 = np.random.uniform(0,1,n), np.random.uniform(0,1,n)
lons = np.array([(2*np.pi*u * (180/np.pi))-180 for u in rand1])
lats = np.array([(np.arccos(2*v-1)*(180/np.pi)) - 90 for v in rand2])

crd = np.array([*zip(lats,lons)])

lats = crd[:,0]
lons = crd[:,1]

lons = lons * u.Unit('deg')
lats = lats * u.Unit('deg')

lons = Longitude(lons)
lats = Latitude(lats)

locs = EarthLocation.from_geodetic(lon=lons, lat=lats)

pos = np.array([locs.get_gcrs(i).cartesian.xyz.value for i in ts])
print(pos.shape)

names = [str(i).zfill(3) for i in range(len(crd))]
bodies = [Body(names[i], pos[:,:,i], times) for i in range(len(locs))]
colors = ['blue']*len(locs)
sizes = [1]*len(locs)

anim = play(bodies, names, colors, sizes, legend=False, path=False)
plt.show()

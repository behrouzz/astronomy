"""
Map of the planets in ICRS
"""


import numpy as np
import matplotlib.pyplot as plt
from astropy.time import Time
from astropy import units as u
from astropy.coordinates import SkyCoord, get_body_barycentric

t = Time.now()

planets = ['mercury','venus','earth','mars','jupiter','saturn','uranus','neptune']
s = np.array([2439, 6052, 6371, 3390, 69911, 58232, 25362, 24622])
sizes = 3 * (np.sqrt(s) / np.sqrt(s).min())
colors = ['black', 'fuchsia', 'green', 'red', 'brown', 'blue', 'cyan', 'indigo']

c = SkyCoord([get_body_barycentric(i, t) for i in planets])
ra = c.ra.wrap_at(180 * u.deg).radian
dec = c.dec.radian

ax, fig = plt.subplots(figsize=(8,4.2), subplot_kw={'projection':'aitoff'})
for i in range(len(planets)):
    plt.plot(ra[i], dec[i], 'o', markersize=sizes[i], c=colors[i], alpha=0.5)
plt.grid(True)
plt.show()


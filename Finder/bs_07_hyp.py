class cns:
    def __init__(self, cns_str):
        self.name = cns_str.split(' ')[0]
        self.num = cns_str.split(' ')[1]
        stars = cns_str.split(' ')[2:]
        self.stars = [int(i) for i in stars]
        self.edges = [tuple(self.stars[i:i+2]) for i in [*range(0,len(self.stars),2)]]



with open('../constellationship.fab', 'r') as f:
    data = f.read().split('\n')[:-1]

dc = {}
for i in data:
    tmp = cns(i)
    dc[tmp.name] = tmp.edges

edges = []
for k,v in dc.items():
    for i in v:
        edges.append(i)

edges_star1 = [i[0] for i in edges]
edges_star2 = [i[1] for i in edges]

#===================================================

from skyfield.api import Star, load, Angle
import pandas as pd
import numpy as np

ts = load.timescale()
t_comet = ts.utc(2020, 7, range(17, 27))
t = t_comet[len(t_comet) // 2]  # middle date

eph = load('../../de421.bsp')
sun = eph['sun']
earth = eph['earth']

df = pd.read_csv('bs_hip_all_selected cols.csv').set_index('hip')
df = df[df['Vmag']<7]
#df = df[df['ra'].notnull()]

ra = Angle(degrees=df['ra'].values)
dec = Angle(degrees=df['dec'].values)

stars = Star(ra=ra, dec=dec)

star_positions = earth.at(t).observe(stars)


#========================================
"""
xy1 = df[['ra', 'dec']].loc[edges_star1].values
xy2 = df[['ra', 'dec']].loc[edges_star2].values
lines_xy = np.rollaxis(np.array([xy1, xy2]), 1)
"""

import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from hypatie.plots import plot_radec, plot_altaz
from hypatie.transform import radec_to_altaz
from hypatie.data import cities

lon, lat = cities['strasbourg'][:2]

marker_size = (0.5 + 7 - df['Vmag'].values) ** 2.0


#ax = plot_radec(ra=df['ra'], dec=df['dec'], mag=df['Vmag'])

t = t.utc_datetime().isoformat()[:19].replace('T', ' ')

alt, az = radec_to_altaz(lon=lon, lat=lat,
                         ra=df['ra'], dec=df['dec'], t=t)

new_df = pd.DataFrame({'hip':df.index.values,
                       'az':az, 'alt':alt, 'Vmag':df['Vmag'].values})
new_df = new_df.set_index('hip')

xy1 = new_df[['az', 'alt']].loc[edges_star1].values
xy2 = new_df[['az', 'alt']].loc[edges_star2].values
lines_xy = np.rollaxis(np.array([xy1, xy2]), 1)

ax = plot_altaz(az, alt, mag=df['Vmag'])

#fig, ax = plt.subplots()
ax.add_collection(LineCollection(lines_xy, colors='#00f2'))
#ax.scatter(df['ra'], df['dec'], s=marker_size, c='k')
plt.show()


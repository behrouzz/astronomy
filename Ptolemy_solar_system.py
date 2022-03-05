from datetime import datetime, timedelta
import numpy as np
import matplotlib.pyplot as plt
from numeph import SPK
from hypatie.animation import Body, play2d
from solsys.transform import equcar_to_eclcar


f = '/path/to/de440s.bsp'

t1 = datetime(2022, 1, 1)
t2 = datetime(2023, 1, 1)

dt = (t2-t1).days
t = [t1 + timedelta(days=i) for i in range(dt)]

spk = SPK(fname=f, t1=t1, t2=t2,
          segs_tup=[(0,10), (0,3), (0,1), (0,2), (0,4), (3, 399)])

# geocentric positions
p3_399 = np.array([spk.segments[(3,399)].get_pos(i) for i in t])
p0_3 = np.array([spk.segments[(0,3)].get_pos(i) for i in t])
# geo_x = p0_x - p3_399 - p0_3

sun = np.array([spk.segments[(0,10)].get_pos(i) for i in t])
mer = np.array([spk.segments[(0, 1)].get_pos(i) for i in t])
ven = np.array([spk.segments[(0, 2)].get_pos(i) for i in t])
mar = np.array([spk.segments[(0, 4)].get_pos(i) for i in t])

geo_sun = sun - p3_399 - p0_3
geo_mer = mer - p3_399 - p0_3
geo_ven = ven - p3_399 - p0_3
geo_mar = mar - p3_399 - p0_3

# Convert to eclitic coordinates
geo_sun = np.array([equcar_to_eclcar(i) for i in geo_sun])
geo_mer = np.array([equcar_to_eclcar(i) for i in geo_mer])
geo_ven = np.array([equcar_to_eclcar(i) for i in geo_ven])
geo_mar = np.array([equcar_to_eclcar(i) for i in geo_mar])

# create animation
bodies = [Body('Earth', np.zeros(geo_sun.shape), t),
          Body('Sun', geo_sun, t),
          Body('Mercury', geo_mer, t),
          Body('Venus', geo_ven, t),
          Body('Mars', geo_mar, t)]

names = ['Earth', 'Sun', 'Mercury', 'Venus', 'Mars']
colors = ['b', 'y', 'k', 'g', 'r']
sizes = [10, 15, 5, 8, 6]

anim = play2d(bodies, names, colors, sizes, path=True)
plt.show()


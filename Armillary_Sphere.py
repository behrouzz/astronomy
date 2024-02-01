#https://commons.wikimedia.org/wiki/File:Armillary-sphere-on-stand.svg

import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
from hypatie import sph2car, unit

stars = [('alf UMa', 165.9319646738126, 61.751034687818226),
         ('bet UMa', 165.46033229797294, 56.382433649496384),
         ('del UMa', 183.85650263625, 57.03261544611111),
         ('eps UMa', 193.5072899675, 55.95982295694445),
         ('eta UMa', 206.88515734206297, 49.31326672942533),
         ('gam UMa', 178.45769715249997, 53.69475972916666),
         ('zet UMa', 200.98141866666666, 54.92535197222222)]

pos = np.zeros((7,3))
pos[:, 0] = [i[1] for i in stars]
pos[:, 1] = [i[2] for i in stars]
pos[:, 2] = 7 * [1e100]

star_positions = np.array([unit(sph2car(i)) for i in pos])


def circle_points(N=100):
    theta = np.linspace(0, 2*np.pi, N)
    x = np.cos(theta)
    y = np.sin(theta)
    return x, y

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

N = 100
x, y = circle_points(N)
z = np.zeros((N,))

obl = np.radians(23)

ax.plot(x, y, z)
ax.plot(x, y*np.cos(obl), y*np.sin(obl))



ax.plot((0,0),(0,0), (-1,1), '-k', label='z-axis')

# draw sphere
u, v = np.mgrid[0:2*np.pi:50j, 0:np.pi:30j]
xx = np.cos(u)*np.sin(v)
yy = np.sin(u)*np.sin(v)
zz = np.cos(v)
ax.plot_wireframe(xx, yy, zz, color="gray", alpha=0.2)


ax.quiver(0, 0, 0, 0, 0, 1, color='r') # CIP vector
ax.quiver(0, 0, 0, 1, 0, 0, color='g') # Equinox vector

# draw a point (Earth)
ax.scatter([0], [0], [0], color="k", s=100)

ax.scatter(star_positions[:,0], star_positions[:,1], star_positions[:,2],
           c='k', s=5)


ax.set_box_aspect((2, 2, 2))
RADIUS = 1.2  # Control value
ax.set_xlim3d(-RADIUS / 2, RADIUS / 2)
ax.set_zlim3d(-RADIUS / 2, RADIUS / 2)
ax.set_ylim3d(-RADIUS / 2, RADIUS / 2)

plt.axis('off')
#ax.legend()
plt.grid(False)
plt.show()

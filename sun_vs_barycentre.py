"""
Sun vs Barycentre of the Solar System
-------------------------------------
We want to create an animation that shows the Sun's position with respect
to the Barycentre of the Solar System during a time window (eg. from 2014 to
2028). You will see that the Barycentre exits the Sun's outline from 2016 and
it will return to it in 2026.

By: Behrouz Safari
"""

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from astropy.coordinates import get_sun
from astropy.time import Time
from astropy import units as u
import seaborn as sns
sns.set()

n = 5000 # length of time_window
t = Time.now()
time_window = t + np.linspace(-7, 7, n)*u.year
x,y,z = get_sun(time_window).icrs.cartesian.xyz.to('km') / 1_000_000
xs_sun, ys_sun, zs_sun = [*x.value], [*y.value], [*z.value]


fig = plt.figure()
fig.set_dpi(100)
fig.set_size_inches(7, 6.5)

ax = plt.axes(xlim=(-2, 2), ylim=(-2, 2))

ax.add_artist(plt.Circle((0, 0), 0.05, color='green'))
ax.set_aspect(1)
patch = plt.Circle((xs_sun[0], ys_sun[0]), 0.696340, color='yellow', alpha=0.8)

ttl = ax.text(0.41, 1.005, '', transform = ax.transAxes)

def init():
    ttl.set_text('')
    patch.center = (0, 0)
    ax.add_patch(patch)
    return patch,

def animate(i):
    ttl.set_text(time_window[i].iso[:10])
    x, y = patch.center
    x = xs_sun[i]
    y = ys_sun[i]
    patch.center = (x, y)
    return patch,

anim = FuncAnimation(fig, animate, init_func=init,
                     frames=range(0, n, 20), interval=1)

plt.xlabel('X (million km)')
plt.ylabel('Y (million km)')
plt.show()

# If you want to save the animation as a mp4 file:
#import matplotlib.animation as animation
#Writer = animation.writers['ffmpeg']
#writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)
#anim.save('Sun_vs_Barycentre.mp4', writer=writer)

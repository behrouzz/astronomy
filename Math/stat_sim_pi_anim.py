import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

N = 1000

x = np.random.uniform(low=-1, high=1, size=N)
y = np.random.uniform(low=-1, high=1, size=N)

fig, ax = plt.subplots()
ax.set_aspect('equal')
plt.ylim(-1.5,1.5)
plt.xlim(-1.5,1.5)
plt.xlabel('X')
plt.ylabel('Y')
plt.grid(alpha=0.5)
plt.figtext(.5,.94,'Statistical simulation for caculating pi', fontsize=12, ha='center')
plt.figtext(.5,.9,'behrouzz.github.io', fontsize=9,ha='center', fontstyle='italic')

circle = plt.Circle((0, 0), 1, color='k', linewidth=2, fill=False)
square = plt.Rectangle((-1,-1), 2, 2, color='k', linewidth=2, fill=False)
ax.add_patch(circle)
ax.add_patch(square)

red = 0
blue = 0
txtN = ax.text(-0.5, 1.25, '')
txt = ax.text(-0.8, 1.1, '')

def run(i):
    global red
    global blue
    if x[i]**2 + y[i]**2 <= 1:
        red += 1
        color = 'red'
    else:
        blue += 1
        color = 'blue'
    pi = 4 * red/(red+blue)
    ax.scatter(x[i], y[i], 10, color=color)
    text = 'pi = 4 * red/N = '+'{:.8f}'.format(pi)
    txtN.set_text('N = red + blue = '+str(red+blue))
    txt.set_text(text)

ani = FuncAnimation(fig=fig, func=run, frames=N,
                    interval=1, repeat=False)
#plt.show()
import matplotlib.animation as animation
Writer = animation.writers['ffmpeg']
writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)
ani.save('pi.mp4', writer=writer)

import pickle
import numpy as np
from datetime import timedelta, datetime
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D


class Simulation:
    '''The main class'''
    def __init__(self, n_days, t):
        self.n_days = n_days
        self.t = t
        self.G = 6.6743e-11
        self.bodies = []
        self.runned = False

    class Body:
        def __init__(self, name, color, size, mass, pos, vel):
            self.name = name
            self.color = color
            self.size = size
            self.m = mass
            self.p = np.array(pos)
            self.pS = [np.array(pos)]
            self.v = np.array(vel)
            self.f = np.array([])
            self.xs = np.array([])
            self.ys = np.array([])
            self.zs = np.array([])

    def add_body(self, name, color, size, mass, pos, vel):
        self.bodies.append(self.Body(name, color, size, mass, pos, vel))

    def force_2bd(self, b1, b2):
        '''Gravitational force acting on b1 from b2'''
        d = np.sqrt(((b2.p-b1.p)[0])**2 + ((b2.p-b1.p)[1])**2 + ((b2.p-b1.p)[2])**2)
        mag_f = (self.G * b1.m * b2.m) / (d**2)
        f = mag_f * (b1.p - b2.p) / d
        return f

    def force_nbd(self, b, bodies):
        '''Gravitational force acting on b from other bodies'''
        fS = []
        for i in bodies:
            if i != b:
                fS.append(self.force_2bd(i, b))
        f = np.array(fS)
        f = np.array([f[:,0].sum(), f[:,1].sum(), f[:,2].sum()])
        return f

    def run(self):
        '''Run the simulation'''
        if len(self.bodies)<2:
            print('You should add at least two bodies')
            exit
        
        t = self.t + np.linspace(0, self.n_days, self.n_days) * timedelta(days=1)
        dt = (t[1] - t[0]).total_seconds()

        for i in range(len(t)):
            for b in self.bodies:
                b.p = b.p + b.v*dt
                b.pS.append(b.p)
            for b in self.bodies:
                b.f = self.force_nbd(b, self.bodies)
            for b in self.bodies:
                b.v = b.v + (b.f/b.m)*dt

        # Convert (1 au = 1.49597871e+11 m) & extracting positions
        for b in self.bodies:
            b.pS = np.array(b.pS)/1.49597871e+11
            b.xs, b.ys, b.zs = b.pS[:,0], b.pS[:,1], b.pS[:,2]

        self.runned = True

    def play(self):
        '''Animation 3d'''
        if not self.runned:
            self.run()
        
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        lines = []
        for b in self.bodies:
            ax.plot(b.xs, b.ys, b.zs, b.color)
            lines.append(ax.plot(b.xs[0:2], b.xs[0:2], b.xs[0:2], b.color+'o', markersize=b.size, label=b.name)[0])

        def init():
            for line in lines:
                line.set_xdata([])
                line.set_ydata([])
                line.set_3d_properties([])
            return lines

        def animate(i):
            for j,line in enumerate(lines):
                line.set_xdata([self.bodies[j].xs[i]])
                line.set_ydata([self.bodies[j].ys[i]])
                line.set_3d_properties([self.bodies[j].zs[i]])
            return lines

        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
        ax.axes.xaxis.set_ticklabels([])
        ax.axes.yaxis.set_ticklabels([])
        ax.axes.zaxis.set_ticklabels([])
        plt.legend()
        plt.grid(True)

        _ = FuncAnimation(fig, animate, init_func=init,
                          frames=self.n_days, interval=20, blit=True, repeat=True)
        plt.show()

#=======================================================
# USING THE LIBRARY
#=======================================================

# Initial conditions
with open('../data/init_inner_planets.pickle', 'rb') as file:
    _,m1,m2,m3,m4,m5,p1,p2,p3,p4,p5,v1,v2,v3,v4,v5 = pickle.load(file)

t = datetime(2020, 1, 1)

ls = [['sun', 'y', 15, m1, p1, v1],
      ['mercury', 'k', 6, m2, p2, v2],
      ['venus', 'g', 8, m3, p3, v3],
      ['earth', 'b', 8, m4, p4, v4],
      ['mars', 'r', 8, m5, p5, v5]]

# Starting the program

sim = Simulation(700, t)

for i in ls:
    name, color, size, mass, pos, vel = i
    sim.add_body(name, color, size, mass, pos, vel)

sim.play()




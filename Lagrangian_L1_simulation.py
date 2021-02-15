from gravitational.simulation import Simulation
from gravitational.utils import unit_vector, magnitude
import numpy as np

def lagrangian(ms, mp, rsp):
    '''
    Returns L1 position(s) of Planet with respect to Star

    ms  : mass of Star
    mp  : mass of Planet
    rsp : distance from Star to Planet
    '''
    L1_1 = rsp*(mp - np.sqrt(mp*ms))/(mp - ms)
    L1_2 = rsp*(mp + np.sqrt(mp*ms))/(mp - ms)
    return [L1_1, L1_2]

m_s = 2e+30
m_p = 5e+28
m = 1000

p_s = (0,0,0)
p_p = (1e11, 0,0)

v_s = (0,0,0)
v_p = (0,1,0)


sim = Simulation('2020-02-15 19:00:00')

star = sim.add_body(name='Star', color='y', size=25,
                    mass=m_s, position=p_s, velocity=v_s)

planet = sim.add_body(name='Planet', color='b', size=8,
                    mass=m_p, position=p_p, velocity=v_p)

sim.set_in_orbit('Planet', 'Star')

v_p = planet.v

L1 = lagrangian(m_s, m_p, sim.distance(star, planet))
print(L1[0]/sim.distance(star, planet))

p = np.array(p_p) - np.array(unit_vector(p_p))*L1[0]
p = tuple(p)
v = ((magnitude(p)-L1[0])*np.array(v_p)) / magnitude(p)
v = tuple(v)

sat = sim.add_body(name='Sat', color='k', size=2,
                    mass=m, position=p, velocity=v)

sim.run(185, 0.1)
sim.play('2d', path=True, interval=5)




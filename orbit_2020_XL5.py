from gravitational.simulation import Simulation
from astroquery.jplhorizons import Horizons
from astropy.constants import M_sun, M_earth
from astropy.time import Time

def initial_condition(h):
    vec = h.vectors(refplane='earth')
    x = vec['x'].to('m').value
    y = vec['y'].to('m').value
    z = vec['z'].to('m').value
    vx = vec['vx'].to('m / s').value
    vy = vec['vy'].to('m / s').value
    vz = vec['vz'].to('m / s').value
    return [(x[0],y[0],z[0]), (vx[0],vy[0],vz[0])]


t = '2020-02-15 01:08:00'
jd = Time(t).jd

sim = Simulation(t)

names = ['Sun', 'venus', 'Earth', '2020 XL5']
colors = ['y', 'r', 'b', 'k']
sizes = [25, 10, 13, 3]
types = ['id', 'id', 'id', 'smallbody']
ids = [10, 299, 399, '2020 XL5']
masses = [M_sun.value, 4.867e+24, M_earth.value, 0.0313*M_earth.value]


bodies = []

for i in range(len(names)):
    h = Horizons(id_type=types[i], id=ids[i], location='500@0', epochs=jd)
    p0,v0 = initial_condition(h)
    bodies.append(sim.add_body(name=names[i], color=colors[i], size=sizes[i],
                               mass=masses[i], position=p0, velocity=v0))


sim.run(duration=365, dt=1)
sim.play('3d', path=True, legend=True)


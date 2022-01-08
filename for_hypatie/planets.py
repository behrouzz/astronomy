from datetime import datetime
from astropy.time import Time
from astropy.coordinates import solar_system_ephemeris, EarthLocation, get_body
from hypatie.transform import radec_to_altaz, radec_to_cartesian
from hypatie.data import cities
import matplotlib.pyplot as plt
from hypatie.plots import plot_altaz

def planet(body, obs_loc, t=None):
    
    if t is None:
        t = datetime.utcnow()
    
    body = body.lower()
    if not body in solar_system_ephemeris.bodies:
        raise Exception("Body not available!")
    
    if type(obs_loc)==str and obs_loc in cities.keys():
        lon, lat = cities[obs_loc][:-1]
    elif isinstance(obs_loc, tuple):
        if len(obs_loc)==2:
            lon, lat = obs_loc
        else:
            raise Exception("obs_loc should be in the format: (lon, lat)")
    else:
        raise Exception("obs_loc should be a city name or geographic coordiantes.")
    
    loc = EarthLocation(lon=lon, lat=lat)
    
    with solar_system_ephemeris.set('jpl'):
        crd = get_body(body, Time(t), loc)
        
    ra  = crd.ra.value
    dec = crd.dec.value
    r   = crd.distance.value
    
    x, y, z = radec_to_cartesian(ra, dec, r)
    alt, az = radec_to_altaz(lon=lon, lat=lat, ra=ra, dec=dec, t=t)
    
    return (x,y,z), (ra,dec,r), (az, alt)
    

def planets(body, loc, t, tt):
    
    with solar_system_ephemeris.set('jpl'):
        crd = get_body(body, tt, loc)
        
    ra  = crd.ra.value
    dec = crd.dec.value
    r   = crd.distance.value
    
    x, y, z = radec_to_cartesian(ra, dec, r)
    alt, az = radec_to_altaz(lon=lon, lat=lat, ra=ra, dec=dec, t=t)
    
    return (x,y,z), (ra,dec,r), (az, alt)


#bodies = ['sun','moon','mercury','venus','mars','jupiter','saturn','uranus','neptune']
bodies = solar_system_ephemeris.bodies

t = datetime.utcnow()
#t = '2022-01-10 17:00:00'
tt = Time(t)
lon, lat = cities['strasbourg'][:-1]
loc = EarthLocation(lon=lon, lat=lat)

ls = []
for body in bodies:
    ls.append(planets(body, loc, t, tt))

az_alt = [i[-1] for i in ls]

for i in range(len(az_alt)):
    if az_alt[i][1]>0: #alt>0
        print(bodies[i])
        print(az_alt[i])
        print('*'*70)

visible = [bodies[i] for i in range(len(bodies)) if az_alt[i][1]>0]
az  = [i[0] for i in az_alt if i[1]>0]
alt = [i[1] for i in az_alt if i[1]>0]

plot_altaz(az, alt)
plt.show()

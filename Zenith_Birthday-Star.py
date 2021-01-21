"""
What is your birthday star?
===========================
For each location on the Earth at a given moment in time, there is a sky
coordinate which is exactly above that point. This point is called 'zenith'.

Imagine that you were born in the location L at the moment T. Here, L is
a geographical coordinate on Earth, represented by two numbers: lattitude and
longtitude. T is a moment in time, so it consists of date and time values.
The EarthLocation in astropy will create the location L for us. Now, we want
to find the zenith of that location in the time T. Using AltAz class in
astropy, we can create a coordinate in the sky based on L and T. The zenith is
always the point in the sky whose altitude is 90 degrees. It doesn't matter
which value for the azimuth you choose.

Now we shoud convert this coordinate to the SkyCoord coordinate in the ICRS
frame to extract the RA and DEC.

Once we have the SkyCoord, we can query the SIMBAD database to find all the
objects located in a circle with a certain raduis centered on our SkyCoord.

The function get_script gives us the SQL (in fact, this is ADQL) script that
we need to query SIMBAD. Note that one of the properties I have selected is
allfluxes.V which is the apparent magnitude. Since we are interested in stars
the are visible by naked eyes, I have created a condion in the WHERE clause
to limit the selection to the apparent magnitude below a certain value.
I have set 6 as the default value for max_magnitude because this is the maximum
value visible with naked eye.

The sencond function will send the SQL script to the SIMBAD server and returns
two pandas DataFrames: meta and df.

Note that radius is in arcmin, and the birth_loc is a tuple with latitude as the
first element and longtitude as the second. 
"""

import requests
import numpy as np
import pandas as pd
from astropy.time import Time
from astropy import units as u
from astropy.coordinates import SkyCoord, EarthLocation, AltAz


def get_script(location, time_str, radius, max_magnitude=6):
    loc = EarthLocation(lat=location[0], lon=location[1])
    t = Time(time_str)
    zenith = AltAz(az=0*u.deg, alt=90*u.deg, obstime=t, location=loc)
    c = SkyCoord(zenith).icrs
    ra = str(c.ra.value)
    dec = '%2D'+str(c.dec.value) if c.dec.value<0 else '%2B'+str(c.dec.value)
    sql = f"""SELECT TOP 10 main_id, ra, dec, otype_txt, plx_value, rvz_redshift,
    allfluxes.V,
    distance(POINT('ICRS',ra,dec), POINT('ICRS',{ra},{dec[3:]})) as dist
    FROM basic
    JOIN allfluxes ON basic.oid=allfluxes.oidref
    WHERE
    CONTAINS(POINT('ICRS',ra,dec), CIRCLE('ICRS',{ra},{dec[3:]},{radius/60}))=1
    AND allfluxes.V < {max_magnitude}
    ORDER BY dist"""
    return sql.replace('\n', ' ')

def get_df(sql):
    base = 'http://simbad.u-strasbg.fr/simbad/sim-tap/sync?'
    base = base + 'request=doQuery&lang=adql&format=json&query='
    r = requests.get(base+sql).json()
    meta = pd.DataFrame(r['metadata'])
    cols = [i['name'] for i in r['metadata']]
    df = pd.DataFrame(r['data'], columns=cols)
    return meta,df


birth_loc = (31.33597564428792, 48.67764926012252)
birth_time = '1981-12-31 22:49:30'
sql = get_script(birth_loc, birth_time, radius=600, max_magnitude=4)
meta, df = get_df(sql)

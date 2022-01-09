# https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/satellites/a_old_versions/
# https://ssd.jpl.nasa.gov/ftp/eph/planets/bsp/
# https://ssd.jpl.nasa.gov/planets/eph_export.html
# https://ssd.jpl.nasa.gov/sats/ephem/

from skyfield.api import load
"""
ts = load.timescale()
t = ts.utc(2022, 2, 26, 15, 19)

planets = load('bsp_files/jup310.bsp')  # ephemeris DE421
print(planets)

astm = planets['JUPITER'].at(t)
"""
s = load('bsp_files/de421.bsp')
print(s)

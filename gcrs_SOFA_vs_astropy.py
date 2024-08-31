from astropy.coordinates import SkyCoord
from astropy.time import Time
from astropy.utils.iers import IERS_A
import erfa
from datetime import datetime


def get_tt(t):
    utc1, utc2 = erfa.dtf2d('UTC', t.year, t.month, t.day, t.hour, t.minute, t.second + (t.microsecond / 1e6))
    tai1, tai2 = erfa.utctai(utc1, utc2)
    tt1, tt2 = erfa.taitt(tai1, tai2)
    return tt1, tt2

def get_gcrs(t, ra, dec, pmra=None, pmdec=None, plx=None, radvel=None):
    rc = ra * erfa.DD2R
    dc = dec * erfa.DD2R
    pr = pmra * faws.DMAS2R if pmra is not None else 0
    pd = pmdec * faws.DMAS2R if pmdec is not None else 0
    px = plx * 0.001 if plx is not None else 0
    rv = radvel if radvel is not None else 0
    
    tt1, tt2 = get_tt(t)
    #astrom, eo = erfa.apci13(tt1, tt2) #DEGHAT
    astrom = erfa.apcg13(tt1, tt2)      #DEGHAT

    # part of "atciq" function
    # Proper motion and parallax, giving BCRS coordinate direction
    pco = erfa.pmpx(rc, dc, pr, pd, px, rv, astrom['pmt'], astrom['eb'])
    # Light deflection by the Sun, giving BCRS natural direction
    pnat = erfa.ldsun(pco, astrom['eh'], astrom['em'])
    # Aberration, giving GCRS proper direction
    ppr = erfa.ab(pnat, astrom['v'], astrom['em'], astrom['bm1'])
    # GCRS RA,Dec
    w, decG = erfa.c2s(ppr)
    raG = erfa.anp(w)
    return raG*erfa.DR2D, decG*erfa.DR2D



# Given data
#------------------------------------
dt = datetime(2024, 2, 10, 22, 32, 37)
t = Time(dt, scale='utc')

iers = IERS_A.open()
dut1 = iers.ut1_utc(t).value
px, py = [i.to('arcsec').value for i in iers.pm_xy(t)]

ra = 101.287155333
dec = -16.716115861
#------------------------------------


# With astropy
c = SkyCoord(ra=ra, dec=dec, unit='deg', frame='icrs', obstime=t)
print('RA  astr:', c.gcrs.ra.deg)
print('DEC astr:', c.gcrs.dec.deg)

# With SOFA
raG, decG = get_gcrs(dt, ra, dec)
print('RA  sofa:', raG)
print('DEC sofa:', decG)


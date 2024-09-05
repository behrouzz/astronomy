import erfa
from iers import EOP
import numpy as np

def printSph(p, text=''):
    w, d = erfa.c2s(p)
    r = erfa.anp(w)
    print(f"{text}: {r*erfa.DR2D}, {d*erfa.DR2D}")

# Step 1: prepare
# ===============
# Star data
rc = 353.22987757 * erfa.DD2R
dc = 52.27730247  * erfa.DD2R
pr = np.arctan2(22.9 * erfa.DMAS2R, np.cos(dc))
pd = -2.1 * erfa.DMAS2R
px = 23.0 * 0.001
rv = 25.0

# Time of observation (convert UTC to TT)
utc1, utc2 = erfa.dtf2d("UTC", 2003, 8, 26, 0, 37, 38.973810)
tai1, tai2 = erfa.utctai(utc1, utc2)
tt1, tt2 = erfa.taitt(tai1, tai2)

# Earth Orientation Parameters
eop = EOP()
dc_eop = eop.get_eop(utc1 + utc2)
dut1 = dc_eop['ut1_utc']
xp = dc_eop['px'] * erfa.DAS2R
yp = dc_eop['py'] * erfa.DAS2R
dx = dc_eop['dx'] * erfa.DMAS2R
dy = dc_eop['dy'] * erfa.DMAS2R

# Step 2: Position-velocites (PVs) of the Earth
# =============================================
# Earth heliocentric and barycentric position-velocity vectors
pvh, pvb = erfa.epv00(tt1, tt2)

# distance from Sun to observer (au) & Sun to observer (unit vector)
em = np.sum(pvh[0]**2) ** 0.5
eh = pvh[0] / em

# barycentric observer velocity (vector, c)
v = pvb[1] / erfa.DC #Note: DC is Speed of light (au per day)

# reciprocal of Lorenz factor
bm1 = np.sqrt(1 - np.sum(v**2))

# Step 3: BCRS coordinates
# ========================
# PM time interval (Julian years)
pmt = ((tt1 - 2451545.0) + tt2) / 365.25

# Proper motion and parallax, giving BCRS coordinate direction
pco = erfa.pmpx(rc, dc, pr, pd, px, rv, pmt, pvb[0])

# Light deflection by the Sun, giving BCRS natural direction
pnat = erfa.ldsun(pco, eh, em)

# Step 4: GCRS coordinates
# ========================
# Aberration, giving GCRS proper direction
ppr = erfa.ab(pnat, v, em, bm1)

# Step 5: CIRS coordinates
# ========================
#r = erfa.pnm06a(tt1, tt2)
#x, y = erfa.bpn2xy(r)
x, y = erfa.xy06(tt1, tt2)

x += dx # Apply IERS corrections
y += dy # Apply IERS corrections
s = erfa.s06(tt1, tt2, x, y)

# More precise BPN matrix -> gives CIRS matrix
bpn = erfa.c2ixys(x, y, s)

# Bias-precession-nutation, giving CIRS proper direction
p_cirs = erfa.rxp(bpn, ppr)

# CIRS RA,Dec
w, di = erfa.c2s(p_cirs)
ri = erfa.anp(w)

### Step 6: Observed coordinates
### ============================
##elong = 9.712156 * erfa.DD2R
##phi = 52.385639  * erfa.DD2R
##hm = 200.0
##phpa = 1000.0 #Ambient pressure (HPa)
##tc = 20.0     #Temperature (C)
##rh = 0.70     #Relative humidity (frac)
##wl = 0.55     #wavelength  (microns)
##
### CIRS to topocentric
##(aot, zot, hot, dot, rot) = erfa.atio13(
##    ri, di, utc1, utc2, dut1,
##    elong, phi, hm, xp, yp,
##    0.0, 0.0, 0.0, 0.0
##)
##print(f"Topocentric: {hot*erfa.DR2D}, {dot*erfa.DR2D}")
##print(f"Topocentric: {aot*erfa.DR2D}, {90-zot*erfa.DR2D}")
##
### CIRS to observed
##(aob, zob, hob, dob, rob) = erfa.atio13(
##    ri, di, utc1, utc2, dut1,
##    elong, phi, hm, xp, yp,
##    phpa, tc, rh, wl
##)
##print(f"Observed   : {aob*erfa.DR2D}, {90-zob*erfa.DR2D}")


# Calculate Earth Rotation Angle (ERA)
ut11, ut12 = erfa.utcut1(utc1, utc2, dut1)
era = erfa.era00(ut11, ut12)

# Apply ERA (gives TIRS matrix)
r_tirs = erfa.rz(era, bpn)

# The TIO locator s’ (positioning TIO on equator of CIP)
sp = erfa.sp00(tt1, tt2)

# polar motion matrix
rpom = erfa.pom00(xp, yp, sp)

# Apply polar motion (gives ITRS matrix)
r_itrs = erfa.rxr(rpom, r_tirs)

# ta inja hame chi doroste
#=============================================================
elong = 9.712156 * erfa.DD2R
phi = 52.385639  * erfa.DD2R
hm = 200.0
phpa = 1000.0 #Ambient pressure (HPa)
tc = 20.0     #Temperature (C)
rh = 0.70     #Relative humidity (frac)
wl = 0.55     #wavelength  (microns)

#adsApio
#-------
r_locap = erfa.rz(elong, r_itrs)
p_locap = erfa.rxp(r_locap, ppr)
printSph(p_locap)

r = r_locap

# Local Earth Rotation Angle (ERAL)
if (r[0,0]!=0.0) or (r[0,1]!=0.0):
    eral = np.arctan2(r[0,1], r[0,0])
else:
    eral = 0.0

# Adjusted longitude
along = erfa.anpm(eral - era)

# Solve for polar motion [X,Y] with respect to local meridian
xpl = np.arctan2(r[0,2], np.sqrt(r[0,0]**2 + r[0,1]**2))
if (r[1,2]!=0.0) or (r[2,2]!=0.0):
    ypl = -np.arctan2(r[1,2], r[2,2])
else:
    ypl = 0.0

##// Functions of latitude
##astrom.sphi = sin(phi)
##astrom.cphi = cos(phi)
##
##// Observer's geocentric position and velocity (m, m/s, CIRS)
##let pv = adsPvtob(elong, phi, hm, xp, yp, sp, theta)
##
##// Magnitude of diurnal aberration vector
##astrom.diurab = sqrt(pv[1][0] * pv[1][0] + pv[1][1] * pv[1][1]) / adsCMPS


# adsAtioq
#---------
# CIRS RA,Dec to Cartesian -HA,Dec (kh: ehtemelan local apparent)
v = erfa.s2c(ri - eral, di)

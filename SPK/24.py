"""
The records within a segment are ordered by increasing initial epoch.
All records contain the same number of coefficients. A segment of this
type is structured as follows:

   +---------------+
   | Record 1      |
   +---------------+
   | Record 2      |
   +---------------+
     ...
   +---------------+
   | Record N      |
   +---------------+
   | INIT          |
   +---------------+
   | INTLEN        |
   +---------------+
   | RSIZE         |
   +---------------+
   | N             |
   +---------------+

A four-number `directory' at the end of the segment contains the information
needed to determine the location of the record corresponding to a particular
epoch.

1. INIT is the initial epoch of the first record, given in ephemeris seconds
   past J2000.
2. INTLEN is the length of the interval covered by each record, in seconds.
3. RSIZE is the total size of (number of array elements in) each record.
4. N is the number of records contained in the segment.

Each record is structured as follows:
   +------------------+
   | MID              |
   +------------------+
   | RADIUS           |
   +------------------+
   | X  coefficients  |
   +------------------+
   | Y  coefficients  |
   +------------------+
   | Z  coefficients  |
   +------------------+

The first two elements in the record, MID and RADIUS, are the midpoint and
radius of the time interval covered by coefficients in the record. These are
used as parameters to perform transformations between the domain of the
record (from MID - RADIUS to MID + RADIUS) and the domain of Chebyshev
polynomials (from -1 to 1 ).

The same number of coefficients is always used for each component, and all
records are the same size (RSIZE), so the degree of each polynomial is
   ( RSIZE - 2 ) / 3 - 1
"""

from jplephem.spk import SPK
import numpy as np

k = SPK.open('de421.bsp')
seg = k[0,3]
#print(seg)

INIT, INTLEN, RSIZE, N = seg.daf.read_array(seg.end_i - 3, seg.end_i)

t_ini, interval, coefficients = seg.load_array()
print(coefficients.shape)

print('INIT, INTLEN, RSIZE, N =', (INIT, INTLEN, RSIZE, N))
#print('init, intlen, coefficients.shape =', seg._data)
print('t_ini, interval, coefficients.shape =', (t_ini, interval, coefficients.shape))
#k.close()

cf_count = int(RSIZE - 2) // 3 #ex: 13
cf = seg.daf.map_array(seg.start_i, seg.end_i - 4)
cf.shape = (int(N), int(RSIZE))
MID_and_RADIUS = cf[:,:2]

MID = MID_and_RADIUS[:,0]
RADIUS = MID_and_RADIUS[:,1]

dom1 = MID - RADIUS
dom2 = MID + RADIUS

old_domains = np.vstack((dom1, dom2)).reshape(MID_and_RADIUS.shape)

domains = np.zeros(MID_and_RADIUS.shape)

for i in range(len(dom1)):
    domains[i,0], domains[i,1] = dom1[i], dom2[i]


# FIRST RECORD
# ============
rec = 0
cfx = coefficients[0,rec,:]
cfy = coefficients[1,rec,:]
cfz = coefficients[2,rec,:]

fx = np.polynomial.chebyshev.Chebyshev(coef=cfx, domain=domains[rec])
fy = np.polynomial.chebyshev.Chebyshev(coef=cfy, domain=domains[rec])
fz = np.polynomial.chebyshev.Chebyshev(coef=cfz, domain=domains[rec])

t = np.linspace(domains[rec,0], domains[rec,1], 5)

X = fx(t)
Y = fy(t)
Z = fz(t)

pos = np.vstack((X,Y,Z)).T

T0 = 2451545.0
S_PER_DAY = 86400.0

def mag(x):
    return np.linalg.norm(np.array(x))

def jd(seconds):
    """Convert a number of seconds since J2000 to a Julian Date."""
    return T0 + seconds / S_PER_DAY

for i in pos:
	print(mag(i))

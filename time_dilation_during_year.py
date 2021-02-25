import numpy as np
from astropy.time import Time
from datetime import datetime, timedelta

N = [str(i).zfill(3) for i in range(1,366)]
dates1 = [datetime(2020,1,1,12,0,0) + timedelta(days=i) for i in range(365)]
dates2 = [datetime(2020,1,1,12,0,1) + timedelta(days=i) for i in range(365)]

dtS = []

for i in range(len(N)):
    t1 = Time(dates1[i], scale='tdb').utc
    t2 = Time(dates2[i], scale='tdb').utc
    dt = t2 - t1
    print('One TDB second in '+N[i]+'th day =', dt.sec, 'UTC seconds')
    dtS.append(dt.sec)

print('='*50)
dtS = np.array(dtS)
print('The shortest:', dates1[np.argmin(dtS)].isoformat()[:10])
print('The longest :', dates1[np.argmax(dtS)].isoformat()[:10])


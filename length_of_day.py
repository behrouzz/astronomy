from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import os
from urllib.request import urlretrieve


file = 'eopc04.62-now'
URL = 'https://hpiers.obspm.fr/iers/eop/eopc04/' + file

if not os.path.isfile(file):
    urlretrieve(URL, file)

with open(file, 'r') as f:
    data = f.read().split('\n')[14:-1]

data = [i[:65] for i in data]

lod = np.array([float(i[-10:]) for i in data])
lod_ms = lod * 1000 # in miliseconds
date = [i[:12].replace('   ', '-') for i in data]
date = [i.replace('  ', '-').replace(' ', '-') for i in date]
date = [i.split('-') for i in date]
dates = []
for i in date:
    dates.append(datetime(int(i[0]), int(i[1]), int(i[2])))
            
plt.plot(dates, lod_ms, lw=0.5)
#plt.scatter(dates, lod_ms, s=5, c='r', alpha=0.5)
plt.title('Length Of Day faster/slower than 24h\n- : shorter than 24h (fast)\n+ : longer than 24h (slow)')
plt.xlabel('Date')
plt.ylabel('Faster than 86400s (milliseconds)')
plt.grid()
plt.show()

# June 29, 2022, is now the shortest day we've seen, at
# more than 1.59 ms faster than the 24-hour standard.

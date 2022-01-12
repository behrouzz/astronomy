class cns:
    def __init__(self, cns_str):
        self.name = cns_str.split(' ')[0]
        self.num = cns_str.split(' ')[1]
        stars = cns_str.split(' ')[2:]
        self.stars = [int(i) for i in stars]
        self.edges = [tuple(self.stars[i:i+2]) for i in [*range(0,len(self.stars),2)]]



with open('constellationship.fab', 'r') as f:
    data = f.read().split('\n')[:-1]

dc = {}
for i in data:
    tmp = cns(i)
    dc[tmp.name] = tmp.edges

edges = []
for k,v in dc.items():
    for i in v:
        edges.append(i)

edges_star1 = [i[0] for i in edges]
edges_star2 = [i[1] for i in edges]

#===================================================

from skyfield.api import Star, load

eph = load('../de421.bsp')
sun = eph['sun']
earth = eph['earth']

import hypatie as hp

#cat = hp.Catalogue(name='hipparcos', where='Vmag < 7', n_max=400000)
cat = hp.Catalogue(name='hipparcos', n_max=1000000)

data, meta = cat.download()

data.set_index('HIP').to_csv('bs_hip_all.csv')

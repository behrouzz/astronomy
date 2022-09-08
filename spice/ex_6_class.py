from datetime import datetime
import spiceypy as sp
import bspice as bs
import numpy as np


d2r = 3.141592653589793/180
r2d = 180/3.141592653589793


class Observe:
    def __init__(self, t, obs_loc, extra_kernels=None):
        
        self.t = t
        self.obs_loc = obs_loc


        self.__vipker = ['bs_kernels/naif0012.tls',
                         'bs_kernels/earth_latest_high_prec.bpc',
                         'bs_kernels/pck00010.tpc']
        #self.__impker = ['bs_kernels/de440s.bsp']
        self.kernels = self.__vipker #+ self.__impker
        if extra_kernels is not None:
            self.kernels = self.kernels + extra_kernels

        for k in self.__vipker:
            sp.furnsh(k)
        self.et = sp.str2et(str(t))
        # J2000 to body-equator-and-prime-meridian coordinates rotation matrix
        self.j2000_to_earthfixed_rot = sp.tisbod(ref='J2000', body=399, et=self.et)[:3,:3]
        self.unload_kernels()
        self.ecef2enu_rot = self.__ecef2enu()


    def load_kernels(self):
        for k in self.kernels:
            sp.furnsh(k)


    def unload_kernels(self):
        sp.kclear()


    def __icrs_or_gcrs(self, body, abcorr, obs):
        self.load_kernels()
        state, lt = sp.spkez(targ=body, et=self.et, ref='J2000', abcorr=abcorr, obs=obs)
        self.unload_kernels()
        pos = state[:3]
        vel = state[3:]
        return pos, vel, lt


    def icrs(self, body, abccorr='NONE'):
        pos, _, _ = self.__icrs_or_gcrs(body=body, abcorr=abccorr, obs=0)
        return pos


    def gcrs(self, body, abccorr='NONE'):
        pos, _, _ = self.__icrs_or_gcrs(body=body, abcorr=abccorr, obs=399)
        return pos
        

    def __ecef2enu(self):
        lon, lat, _ = self.obs_loc
        lon = lon * d2r
        lat = lat * d2r
        r1 = [-np.sin(lon), np.cos(lon), 0]
        r2 = [-np.cos(lon)*np.sin(lat), -np.sin(lon)*np.sin(lat), np.cos(lat)]
        r3 = [np.cos(lon)*np.cos(lat), np.sin(lon)*np.cos(lat), np.sin(lat)]
        return np.array([r1, r2, r3])


    def __enu2aer(self, pos_enu):
        e, n, u = pos_enu
        r = np.hypot(e, n)
        slant_rng = np.hypot(r, u)
        el = np.arctan2(u, r)
        az = np.mod(np.arctan2(e, n), 2*np.pi)
        return az, el, slant_rng


    def get_itrf(self, pos_gcrs):
        return np.matmul(self.j2000_to_earthfixed_rot, pos_gcrs)

    def get_enu(self, pos_gcrs):
        pos_itrf = self.get_itrf(pos_gcrs)
        return np.matmul(self.ecef2enu_rot, pos_itrf)


    def get_altaz(self, pos_gcrs):
        pos_enu = self.get_enu(pos_gcrs)
        az, el, rng = self.__enu2aer(pos_enu)
        return az*r2d, el*r2d, rng


t = datetime.utcnow()
obs_loc = (7.744083817548831, 48.58313582900411, 140)

extra_kernels = ['C:/Moi/_py/Astronomy/Solar System/SPK/data/de440s.bsp',
                 'C:/Moi/_py/Astronomy/Solar System/SPK/data/jup380s.bsp']

o = Observe(t, obs_loc, extra_kernels=extra_kernels)

g = o.gcrs(599)
print(o.get_altaz(g))

"""
Calculating the Particle Horizon
================================
Imagine a photon of light (or any type of particle) has been emitted at the
first moment of beginning of the Universe, i.e, when the Big Bang happened. 
What is the maximum distance that this particle could have traveled to reach 
us at the current moment? We call this distance "Particle Horizon". This is 
a horizon which defines the frontier of our observable universe: a borderline 
beyond which we can not see anything.

If we multiply the age of Universe by the speed of light, we will get a 
distance less than 14 billion light-years. But it is NOT the 'Particle
Horizone'. In fact, we can observe objects far beyond it.

To calculate the Particle Horizon, you can not simply multiply the age of
Universe by the speed of light. Why? Because the Universe is not static. It
is expanding!

So, in order to calculate the Particle Horizone, we need to use the concept
of 'Proper Distance'. Proper Distance is measured at a specific moment in
the cosmic time t. Imagine a distant galaxy which emitted light at time 'te'
and we see that light today at time 't0' (current time). Our distance to the
galaxy is caculated with this formula:

dp(t0) = c * ∫ dt/a(t)  | from te to t0

where,

dp(t0) : our current distance to the galaxy
c      : the speed of light in vacuum
a(t)   : the scale factor
te     : the moment that the light has been emitted from the galaxy
t0     : the moment that the light has reached us

Note that the scale factor is a function in terms of time and it depends
on the model of universe that you choose.


If we put te = 0, it means that we want to calculate our distance from an
object that has emitted a photon exactly at the birth of the universe. 
So we will get the Particle Horizon.

Here, I will use the standard model of the Universe, based on the parameters
measured by Planck spacecraft between 2009 and 2013. First of all, I define
a time window from Big Bang to our time. Then I create the scale factor as
a function of time. Next, by integrating the formula from 'te' to 't0', I find
the proper distance (which is here, the Particle Horizon). At the last line I 
convert it to light-years. We find the radius of the observable universe: 

44.66 billion light-years!

Behrouz Safari
Strasbourg, 17/01/2021
behrouzz.github.io
"""

import numpy as np
from astropy.cosmology import Planck13 as cosmo
from astropy.cosmology import z_at_value
from astropy.constants import c
from astropy import units as u
import scipy.integrate as integrate

# Time window
t = np.linspace(0, cosmo.age(0).to('s'), 10000)[1:-1].value

# scale factor function in terms of t
a = lambda i: cosmo.scale_factor(z_at_value(cosmo.age, i*u.Unit("s")))

te = t[0]  # Big Bang
t0 = t[-1] # Today

# proper distance formula
dp0 = c.value * integrate.quad(lambda i: 1/a(i), te, t0)[0]

# Convert to billion light-years
print(dp0*u.Unit('m').to('lyr')/(10**9), 'billion light-years')

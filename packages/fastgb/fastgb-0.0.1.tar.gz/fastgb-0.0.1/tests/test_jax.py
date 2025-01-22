import time
import numpy as np
import jax.numpy as jnp

from lisaorbits import EqualArmlengthOrbits
from fastgb import fastgb

pGB = np.array(
    [
        0.00135962,  # f0 Hz
        8.94581279e-19,  # fdot "Hz^2
        1.07345e-22,  # ampl strain
        0.312414,  # eclipticlatitude radian
        -2.75291,  # eclipticLongitude radian
        3.5621656,  # polarization radian
        0.523599,  # inclination radian
        3.0581565,  # initial phase radian
    ]
)

fgb = fastgb.FastGB(delta_t=5, T=365 * 24 * 3600, N=128, orbits=EqualArmlengthOrbits())


def test_nojax():
    t0 = time.time()
    for i in range(10):
        X, Y, Z, kmin = fgb.get_fd_tdixyz(pGB.reshape(1, -1))
    t1 = time.time()
    assert (t1 - t0) / 10 < 0.01


def test_jax():
    t0 = time.time()
    for i in range(10):
        X, Y, Z, kmin = fgb.get_fd_tdixyz(jnp.array(pGB).reshape(1, -1))
    t1 = time.time()
    assert (t1 - t0) / 10 > 0.01

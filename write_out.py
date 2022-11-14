#%%
import numpy as np

from swiftsimio import Writer
from swiftsimio.units import cosmo_units

import unyt

xs = np.array([])
ys = np.array([])
IMAGE_SIZE = 256

# Box is image_size cm
boxsize = IMAGE_SIZE * unyt.cm

# Generate object. cosmo_units corresponds to default Gadget-oid units
# of 10^10 Msun, Mpc, and km/s
x = Writer(cosmo_units, boxsize, dimension=2)

# 32^3 particles.
n_p = len(xs)

# Randomly spaced coordinates from 0, 100 Mpc in each direction
x.gas.coordinates = np.array([xs, ys, np.zeros_like(xs)]).T * unyt.cm

# Random velocities from 0 to 1 km/s
# x.gas.velocities = (
#     np.array(
#         [
#             3.0 * ((ys > IMAGE_SIZE * 0.5) - 0.5),
#             10.0 * ((xs > IMAGE_SIZE * 0.5) - 0.5),
#             np.zeros_like(xs),
#         ]
#     ).T
#     * (unyt.cm / unyt.s)
# )
x.gas.velocities = np.array(
    [np.random.rand(len(xs)), np.random.rand(len(xs)), np.zeros(len(xs))]
).T * (unyt.cm / unyt.s)

# Generate uniform masses as 10^6 solar masses for each particle
x.gas.masses = np.ones(n_p, dtype=float) * unyt.g

# Generate internal energy corresponding to 10^4 K
x.gas.internal_energy = np.ones(n_p, dtype=float) * (unyt.cm / unyt.s) ** 2

#
x.gas.smoothing_length = np.ones(len(xs)) * unyt.cm

# If IDs are not present, this automatically generates
x.write("test.hdf5")
# %%

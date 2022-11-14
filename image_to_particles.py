#%%
import PIL
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import swiftascmaps

IMAGE_SIZE = 256
# %%
image = PIL.Image.open("./test.jpeg")
resized = image.resize((IMAGE_SIZE, IMAGE_SIZE))
grayscale = PIL.ImageOps.grayscale(resized)
posterized = PIL.ImageOps.posterize(grayscale, 2)

#%%
plt.imshow(posterized)
# %%
densities = (np.array(posterized) // (256 // 4)) + 1
# %%
xs = []
ys = []
for x in np.arange(IMAGE_SIZE):
    for y in np.arange(IMAGE_SIZE):
        density = densities[x, y]

        these_xs, these_ys = np.meshgrid(
            *[(np.arange(density) + 0.5) / float(density)] * 2
        )

        xs.extend(list((these_xs + float(x)).flat))
        ys.extend(list((these_ys + float(y)).flat))

xs = np.array(xs)
ys = np.array(ys)


# %%
fig, ax = plt.subplots(figsize=(4, 4))
fig.subplots_adjust(0, 0, 1, 1)
ax.axis("off")
plt.hist2d(ys, -xs, norm=LogNorm(), bins=256)  # , cmap="swift.evermore_shifted")
# %%
# Now create swift ics

#%%
from swiftsimio import Writer
from swiftsimio.units import cosmo_units

import unyt

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

import logging

log = logging.getLogger(__name__)
import numpy as np
import matplotlib.pyplot as plt

from starwinds_readplt.dataset import Dataset, auto_coords, triangles


def plot(file, pngfile, u_name, v_name, w_name, wscale):

    log.info(f"Opening data file {file}")
    ds = Dataset.from_file(file)

    if u_name is None and v_name is None:
        u_name, v_name = auto_coords(ds)

    tris = triangles(ds, u_name, v_name)

    _, ax = plt.subplots()

    w_var = ds.variable(w_name)

    if wscale == "log":
        assert np.log10(10) == 1
        w_var = np.log10(w_var)
        w_name = "log10 " + w_name

    img = ax.tricontourf(tris, w_var, levels=100)
    cax = plt.colorbar(img)

    ax.set_title(ds.title + "\n" + str(file) + " " + ds.zone)
    ax.set_xlabel(u_name)
    ax.set_ylabel(v_name)
    ax.set_aspect("equal")
    cax.set_label(w_name)
    log.info(f"Saving figure {pngfile}.")
    plt.savefig(pngfile)
    plt.close()

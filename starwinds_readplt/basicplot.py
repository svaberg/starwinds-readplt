import numpy as np
import matplotlib.pyplot as plt
from matplotlib import tri
import logging
from starwinds_readplt.dataset import Dataset

log = logging.getLogger(__name__)


def auto_coords(ds):
    if np.allclose(ds.variable("X [R]"), 0):
        return "Y [R]", "Z [R]"
    if np.allclose(ds.variable("Y [R]"), 0):
        return "X [R]", "Z [R]"
    if np.allclose(ds.variable("Z [R]"), 0):
        return "X [R]", "Y [R]"


def triangles(ds, uname=None, vname=None):
    """ """

    if uname is None and vname is None:
        uname, vname = auto_coords(ds)

    pu = ds.variable(uname)
    pv = ds.variable(vname)

    if ds.corners.shape[1] != 4:
        raise ValueError("Can only triangulate a 2D dataset with 4 corners per element")

    triangles = np.vstack((ds.corners[:, [0, 1, 2]], ds.corners[:, [2, 3, 0]]))
    return tri.Triangulation(pu, pv, triangles)


def plot(file, pngfile, u_name, v_name, w_name, wscale):

    log.debug(f'Opening data file "{file}".')
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

    img = ax.tripcolor(tris, w_var, shading="gouraud")
    cax = plt.colorbar(img)
    cax.set_label(w_name)

    ax.set_title(ds.title + "\n" + str(file) + " " + ds.zone)
    ax.set_xlabel(u_name)
    ax.set_ylabel(v_name)
    ax.set_aspect("equal")
    log.info(f'Saving figure "{pngfile}".')
    plt.savefig(pngfile)
    plt.close()

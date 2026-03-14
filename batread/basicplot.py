"""Plotting helpers for quick 2D BATSRUS visualizations."""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import tri
import logging
from batread.dataset import Dataset

log = logging.getLogger(__name__)


def auto_coords(ds, names=None):
    """Pick non-zero coordinate variables from a candidate name list."""

    if names is None:
        names = "X [R]", "Y [R]", "Z [R]"

    all_zero = [np.allclose(ds[name], 0) for name in names]
    return np.array(names)[np.logical_not(all_zero)]


def triangles(ds, uname=None, vname=None):
    """Build a triangulation from quadrilateral connectivity."""

    if uname is None and vname is None:
        uname, vname = auto_coords(ds)

    pu = ds[uname]
    pv = ds[vname]

    if ds.corners.shape[1] != 4:
        raise ValueError("Can only triangulate a 2D dataset with 4 corners per element")

    triangles = np.vstack((ds.corners[:, [0, 1, 2]], ds.corners[:, [2, 3, 0]]))
    return tri.Triangulation(pu, pv, triangles)


def plot(file, pngfile, u_name, v_name, w_name, wscale, identifier=None):
    """Render a quick scalar-field plot from a .dat/.plt file."""
    log.debug(f'Opening data file "{file}".')
    try:
        ds = Dataset.from_file(file)
    except ValueError as e:
        log.error(f"Failed to read dataset from file {file}: {e}")
        return

    if u_name is None and v_name is None:
        u_name, v_name = auto_coords(ds)

    tris = triangles(ds, u_name, v_name)

    _, ax = plt.subplots()

    w_var = ds[w_name]

    if wscale == "log":
        assert np.log10(10) == 1
        w_var = np.log10(w_var)
        w_name = "log10 " + w_name

    img = ax.tripcolor(tris, w_var, shading="gouraud")
    cax = plt.colorbar(img)
    cax.set_label(w_name)

    title_lines = [f"{file} {ds.zone}"]
    if ds.title is not None:
        title_lines.insert(0, ds.title)
    if identifier is not None:
        title_lines.append(str(identifier))
    ax.set_title("\n".join(title_lines))

    ax.set_xlabel(u_name)
    ax.set_ylabel(v_name)
    ax.set_aspect("equal")
    log.info(f'Saving figure "{pngfile}".')
    plt.savefig(pngfile)
    plt.close()

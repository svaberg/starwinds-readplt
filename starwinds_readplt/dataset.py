import numpy as np
from matplotlib import tri

from starwinds_readplt.read_dat import read_dat
from starwinds_readplt.read_plt import read_plt


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


class Dataset:
    def __init__(self, points, corners, aux, title, variables, zone):
        self.points = points
        self.corners = corners
        self.aux = aux
        self.title = title
        self.variables = variables
        self.zone = zone

    def __str__(self):
        s = [
            f"Title:     '{self.title}'",
            f"Zone:      '{self.zone}'",
            f"Variables: {len(self.variables)}",
            f"Shape:     {self.points.shape}",
            f"Variables: {self.variables}.",
        ]
        return "\n".join(s)

    @classmethod
    def from_file(cls, file):
        if file.split(".")[-1] == "dat":
            return cls.from_dat(file)
        elif file.split(".")[-1] == "plt":
            return cls.from_plt(file)
        else:
            raise ValueError(f"Unknown extension for file {file}.")

    @classmethod
    def from_dat(cls, file):
        points, corners, aux, title, variables, zone = read_dat(file)
        return cls(points, corners, aux, title, variables, zone)

    @classmethod
    def from_plt(cls, file):
        points, corners, aux, title, variables, zone = read_plt(file)
        return cls(points, corners, aux, title, variables, zone)

    def variable(self, index_or_name):

        try:
            index = int(index_or_name)
            return self.points[:, index]
        except ValueError:
            pass

        try:
            index = self.variables.index(index_or_name)
            return self.points[:, index]
        except ValueError:
            pass

        raise IndexError(f'Variable \'{index_or_name}\' not in dataset. Available variables are {self.variables}.')

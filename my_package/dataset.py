from my_package.read_dat import read_dat
from my_package.read_plt import read_plt


import numpy as np
from matplotlib import tri
def triangles(ds, uname="Y [R]", vname="Z [R]"):
    
    pu = ds.variable(uname)
    pv = ds.variable(vname)

    triangles = np.vstack((ds.corners[:, [0, 1, 2]], ds.corners[:, [2, 3, 0]])) 
    return tri.Triangulation(pu, pv, triangles)


class Dataset():

    def __init__(self, points, corners, aux, title, variables, zone):
        self.points = points
        self.corners = corners
        self.aux = aux
        self.title = title
        self.variables = variables
        self.zone = zone

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

    def variable(self, name):
        index = self.variables.index(name)
        return self.points[:, index]

import numpy as np
import matplotlib.pyplot as plt

from starwinds_readplt.quick_plots import plot
from starwinds_readplt.dataset import Dataset
from starwinds_readplt.dataset import triangles

import pytest


def test2():
    ds = Dataset.from_dat("examples/x=0_var_2_n00000000.dat")
    tris = triangles(ds)
    plot(ds.variable("U_x [km/s]"), tris)
    # plt.show()

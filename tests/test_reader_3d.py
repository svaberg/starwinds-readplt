from typing import Any

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import tri

from time import perf_counter
from contextlib import contextmanager

from starwinds_readplt.read_dat import read_dat
from starwinds_readplt.read_plt import read_plt


@contextmanager
def catchtime() -> float:
    start = perf_counter()
    yield lambda: perf_counter() - start


def test_read_3d_dat():
    filename = "examples/3d__var_1_n00000000.dat"
    points, corners, aux, title, variables, zone_name = read_dat(filename)

    assert np.min(corners) == 0
    assert np.max(corners) + 1 == points.shape[0]

    assert points.shape == (12800, 24)
    assert corners.shape == (12288, 8)


def test_compare_dat_and_plt():
    filename = "examples/3d__var_1_n00000000.dat"
    dpoints, dcorners, daux, dtitle, dvariables, dzone_name = read_dat(filename)

    filename = "examples/3d__var_1_n00000000.plt"
    points, corners, aux, title, variables, zone_name = read_plt(filename)

    assert daux == aux
    assert dtitle == title
    assert dvariables == variables
    assert dzone_name == zone_name

    assert np.allclose(dpoints, points)
    assert np.allclose(dcorners, corners)


def test_3d_point_cloud():
    filename = "examples/3d__var_1_n00000000.plt"

    with catchtime() as t:
        points, corners, *_ = read_plt(filename)
    print(f"Execution time: {t():.4f} secs")

    fig, axs = plt.subplots(2, 2, figsize=(8, 8))
    x = points[:, 0]
    y = points[:, 1]
    z = points[:, 2]

    axs[0, 0].plot(x, y, ".")
    axs[0, 1].plot(x, z, ".")
    axs[1, 0].plot(y, z, ".")
    # axs[1,1].plot(x, y, ',')
    plt.show()
    return fig, axs

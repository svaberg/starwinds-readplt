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


def test_read():
    filename = "examples/x=0_var_2_n00000000.dat"
    dpoints, dcorners, *_ = read_dat(filename)
    # print(dpoints.shape)
    # print(dcorners.shape)
    # print(dpoints)

    filename = "examples/x=0_var_2_n00000000.plt"
    points, corners, *_ = read_plt(filename)
    # print(points.shape)
    # print(corners.shape)
    # print(points)

    assert np.allclose(dpoints, points)
    assert np.allclose(dcorners, corners)


def test_timing():
    filename = "examples/x=0_var_2_n00000000.plt"

    with catchtime() as t:
        points, corners, *_ = read_plt(filename)
    print(f"Execution time: {t():.4f} secs")

    with catchtime() as t:
        triangles = np.vstack((corners[:, [0, 1, 2]], corners[:, [2, 3, 0]]))
        triang = tri.Triangulation(points[:, 1], points[:, 2], triangles)
    print(f"Execution time: {t():.4f} secs")

    with catchtime() as t:
        fig, ax = plt.subplots(figsize=(8, 8))
        u = (points[:, 4] ** 2 + points[:, 5] ** 2 + points[:, 6] ** 2) ** 0.5
        img = ax.tricontourf(triang, u, levels=100)
        plt.colorbar(img)
        ax.set_aspect("equal")
        plt.savefig("test_timing.png")
    print(f"Execution time: {t():.4f} secs")

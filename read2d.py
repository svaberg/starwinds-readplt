import numpy as np
import matplotlib.pyplot as plt
from matplotlib import tri

from time import perf_counter
from contextlib import contextmanager

from my_package.read_dat import read_dat
from my_package.read_plt import read_plt

@contextmanager
def catchtime() -> float:
    start = perf_counter()
    yield lambda: perf_counter() - start

def test1():
    filename = "examples/x=0_var_2_n00000000.dat"
    dpoints, dcorners = read_dat(filename)
    #print(dpoints.shape)
    #print(dcorners.shape)
    #print(dpoints)

    filename = "examples/x=0_var_2_n00000000.plt"
    points, corners = read_plt(filename)
    #print(points.shape)
    #print(corners.shape)
    #print(points)

    assert np.allclose(dpoints, points)
    assert np.allclose(dcorners, corners)


def test2():
    filename = "examples/x=0_var_2_n00000000.plt"
    points, corners = read_plt(filename)

    u = (points[:, 4]**2 + points[:, 5]**2 + points[:, 6]**2)**.5
    triangles = np.vstack((corners[:, [0, 1, 2]], corners[:, [2, 3, 0]])) 
    triang = tri.Triangulation(points[:, 1], points[:, 2], triangles)

    fig, ax = plt.subplots(figsize=(8,8))
    img = ax.tricontourf(triang, u, levels=100)
    plt.colorbar(img)
    ax.triplot(triang, color='k', linewidth=.1)
    return fig, ax


def test3():
    filename = "examples/z=0_var_3_n00000000.plt"
    points, corners = read_plt(filename)

    u = (points[:, 4]**2 + points[:, 5]**2 + points[:, 6]**2)**.5
    triangles = np.vstack((corners[:, [0, 1, 2]], corners[:, [2, 3, 0]])) 
    triang = tri.Triangulation(points[:, 0], points[:, 1], triangles)

    fig, ax = plt.subplots(figsize=(8,8))
    img = ax.tricontourf(triang, u, levels=100)
    plt.colorbar(img)
    ax.triplot(triang, color='k', linewidth=.1)
    return fig, ax  # plt.show()


def test4():
    filename = "examples/x=0_var_2_n00009000.plt"
    points, corners = read_plt(filename)

    u = (points[:, 4]**2 + points[:, 5]**2 + points[:, 6]**2)**.5
    triangles = np.vstack((corners[:, [0, 1, 2]], corners[:, [2, 3, 0]])) 
    triang = tri.Triangulation(points[:, 1], points[:, 2], triangles)

    fig, ax = plt.subplots(figsize=(8,8))
    img = ax.tricontourf(triang, u, levels=100)
    plt.colorbar(img)
    # ax.triplot(triang, color='k', linewidth=.1)
    return fig, ax  # plt.show()


def test5():
    filename = "examples/x=0_var_1_n00094500.plt"

    with catchtime() as t:
        points, corners = read_plt(filename)
    print(f"Execution time: {t():.4f} secs")


    with catchtime() as t:
        triangles = np.vstack((corners[:, [0, 1, 2]], corners[:, [2, 3, 0]])) 
        triang = tri.Triangulation(points[:, 1], points[:, 2], triangles)
    print(f"Execution time: {t():.4f} secs")

    with catchtime() as t:
        fig, ax = plt.subplots(figsize=(8,8))
        u = (points[:, 4]**2 + points[:, 5]**2 + points[:, 6]**2)**.5
        img = ax.tricontourf(triang, u, levels=100)
        plt.colorbar(img)
        ax.set_aspect("equal")
    print(f"Execution time: {t():.4f} secs")
    return fig, ax  # plt.show()


if __name__ == "__main__":

    # test1()

    # test2()

    # test3()

    # test4()

    # plt.close('all')
    test5()
    plt.show()

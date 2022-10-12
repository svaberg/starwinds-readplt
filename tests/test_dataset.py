import numpy as np
from my_package.dataset import Dataset
from my_package.dataset import triangles

import pytest

import matplotlib.pyplot as plt
def plot(data, triangles):    
    fig, ax = plt.subplots()
    img = ax.tricontourf(triangles, data, levels=100)
    plt.colorbar(img)
    ax.triplot(triangles, color='k', linewidth=.1)
    return fig, ax


def test1():
    ds = Dataset.from_dat("examples/x=0_var_2_n00000000.dat")
    y = ds.variable("Y [R]")
    z = ds.variable("Z [R]")
    rho = ds.variable("Rho [g/cm^3]")

def test2():
    ds = Dataset.from_dat("examples/x=0_var_2_n00000000.dat")
    tris = triangles(ds)
    plot(ds.variable("U_x [km/s]"), tris)
    plt.show()

@pytest.mark.parametrize("file", ("examples/x=0_var_2_n00000000.dat", "examples/x=0_var_2_n00000000.plt"))
def test3(file):
    ds = Dataset.from_file(file)

def test_equal():
    ds_dat = Dataset.from_file("examples/x=0_var_2_n00000000.dat")
    ds_plt = Dataset.from_file("examples/x=0_var_2_n00000000.plt")

    assert ds_dat.variables == ds_plt.variables
    assert ds_dat.title == ds_plt.title
    assert ds_dat.zone == ds_plt.zone

    for k, v in ds_dat.aux.items():
        if k == "SAVEDATE":
            continue  # This may not be the same depending on how the files were created
        if k == "NPROC":
            continue  # This may not be the same depending on how the files were created
        assert ds_plt.aux[k] == v, f"Comparing aux {k}."
    
    assert np.allclose(ds_dat.points, ds_plt.points)
    assert np.allclose(ds_dat.corners, ds_plt.corners)


def test_aux():
    ds_dat = Dataset.from_file("examples/x=0_var_2_n00000000.dat")
    ds_plt = Dataset.from_file("examples/x=0_var_2_n00000000.plt")

    assert ds_dat.aux == ds_plt.aux
import numpy as np
import glob
from starwinds_readplt.dataset import Dataset

import pytest


def test_read_variables():
    ds = Dataset.from_dat("examples/x=0_var_2_n00000000.dat")
    y = ds.variable("Y [R]")
    z = ds.variable("Z [R]")
    rho = ds.variable("Rho [g/cm^3]")


def example_files(folder="examples"):
    plt_files = glob.glob(f"{folder}/*.plt")
    dat_files = glob.glob(f"{folder}/*.dat")
    return sorted(plt_files + dat_files)


@pytest.mark.parametrize("file", example_files())
def test_read_files(file):
    ds = Dataset.from_file(file)


def test_data_equal():
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


def test_aux_equal():
    ds_dat = Dataset.from_file("examples/x=0_var_2_n00000000.dat")
    ds_plt = Dataset.from_file("examples/x=0_var_2_n00000000.plt")

    assert ds_dat.aux == ds_plt.aux

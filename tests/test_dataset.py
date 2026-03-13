"""Dataset API regression tests."""

import numpy as np
import glob
from batread.dataset import Dataset

import pytest


def test_read_variables():
    """Verify named variable access returns data."""
    ds = Dataset.from_dat("examples/x=0_var_2_n00000000.dat")

    y = ds.variable("Y [R]")
    assert len(y) > 0

    z = ds.variable("Z [R]")
    assert len(z) > 0

    rho = ds.variable("Rho [g/cm^3]")
    assert len(rho) > 0


def example_files(folder="examples"):
    """Return all example .dat and .plt files."""
    plt_files = glob.glob(f"{folder}/*.plt")
    dat_files = glob.glob(f"{folder}/*.dat")
    return sorted(plt_files + dat_files)


@pytest.mark.parametrize("file", example_files())
def test_read_files(file):
    """Verify each example file exposes non-empty variables."""
    ds = Dataset.from_file(file)
    assert len(ds.variables) > 0

    for vname in ds.variables:
        vdata = ds.variable(vname)
        assert len(vdata) > 0


def test_data_equal():
    """Check that paired .dat and .plt files decode to equal data."""
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
    """Check aux metadata equality for the reference 2D dataset."""
    ds_dat = Dataset.from_file("examples/x=0_var_2_n00000000.dat")
    ds_plt = Dataset.from_file("examples/x=0_var_2_n00000000.plt")

    assert ds_dat.aux == ds_plt.aux

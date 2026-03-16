"""Dataset API regression tests."""

import numpy as np
from batread import Dataset
from conftest import sample_path, with_sample_files, with_sample_pairs


def test_read_variables():
    """Verify named variable access returns data."""
    ds = Dataset.from_dat(sample_path("x=0_var_2_n00000000.dat"))

    y = ds["Y [R]"]
    assert len(y) > 0

    z = ds["Z [R]"]
    assert len(z) > 0

    rho = ds["Rho [g/cm^3]"]
    assert len(rho) > 0


def test_read_variable_slice():
    """Verify integer slices return a variable block."""
    ds = Dataset.from_dat(sample_path("x=0_var_2_n00000000.dat"))

    xyz = ds[0:3]
    assert xyz.shape == (ds.points.shape[0], 3)
    assert np.allclose(xyz, ds.points[:, 0:3])


def test_read_variable_list():
    """Verify lists of variable names return the selected block."""
    ds = Dataset.from_dat(sample_path("x=0_var_2_n00000000.dat"))

    xyz = ds[["X [R]", "Y [R]", "Z [R]"]]
    assert xyz.shape == (ds.points.shape[0], 3)
    assert np.allclose(xyz, ds.points[:, 0:3])


@with_sample_files
def test_read_files(file):
    """Verify each example file exposes non-empty variables."""
    ds = Dataset.from_file(file)
    assert len(ds.variables) > 0

    for vname in ds.variables:
        vdata = ds[vname]
        assert len(vdata) > 0


@with_sample_pairs
def test_data_equal(dat_file, plt_file):
    """Check that paired .dat and .plt files decode to equal data."""
    ds_dat = Dataset.from_file(dat_file)
    ds_plt = Dataset.from_file(plt_file)

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


@with_sample_pairs
def test_aux_equal(dat_file, plt_file):
    """Check aux metadata equality for paired sample datasets."""
    ds_dat = Dataset.from_file(dat_file)
    ds_plt = Dataset.from_file(plt_file)

    assert ds_dat.aux == ds_plt.aux

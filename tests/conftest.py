"""Shared test helpers for sample BATSRUS data files."""

from pathlib import Path

import pytest

SAMPLE_DATA_DIR = Path("sample_data")


def sample_path(filename):
    """Return the path to one sample data file."""

    return str(SAMPLE_DATA_DIR / filename)


def sample_files():
    """Return all sample .dat and .plt files."""
    return sorted(
        str(path)
        for path in SAMPLE_DATA_DIR.iterdir()
        if path.suffix in {".dat", ".plt"}
    )


def sample_pairs():
    """Return matched (.dat, .plt) sample file pairs by stem."""
    dat_files = {path.stem: path for path in SAMPLE_DATA_DIR.glob("*.dat")}
    plt_files = {path.stem: path for path in SAMPLE_DATA_DIR.glob("*.plt")}
    stems = sorted(dat_files.keys() & plt_files.keys())
    return [(str(dat_files[stem]), str(plt_files[stem])) for stem in stems]


def with_sample_files(test):
    """Parametrize a test over all sample .dat and .plt files."""

    return pytest.mark.parametrize("file", sample_files())(test)


def with_sample_pairs(test):
    """Parametrize a test over matched sample (.dat, .plt) file pairs."""

    return pytest.mark.parametrize(("dat_file", "plt_file"), sample_pairs())(test)

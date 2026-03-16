"""CLI smoke tests."""

from pathlib import Path

import pytest


@pytest.mark.parametrize("ext", ("dat", "plt"))
def test_dat(script_runner, ext):
    """Check that the quick-plot CLI succeeds for both file types."""
    ret = script_runner.run(
        ["bat-quick", "x=0_var_2_n00000000." + ext], cwd="sample_data"
    )
    assert ret.success


def test_dat_without_title(script_runner, tmp_path):
    """Check that plotting works for .dat files without a TITLE line."""
    datfile = tmp_path / "slice.dat"
    datfile.write_text(
        "\n".join(
            [
                'VARIABLES = "X [R]", "Y [R]", "Z [R]", "Rho [g/cm^3]"',
                'ZONE T="2D X", N=4, E=1',
                "0 0 0 1",
                "0 1 0 2",
                "0 1 1 3",
                "0 0 1 4",
                "1 2 3 4",
            ]
        )
        + "\n"
    )

    ret = script_runner.run(["bat-quick", datfile.name], cwd=str(tmp_path))

    assert ret.success
    assert [path.name for path in Path(tmp_path).glob("ql-*.png")] == [
        "ql-slice-dat-rho-g-cm-3.png"
    ]

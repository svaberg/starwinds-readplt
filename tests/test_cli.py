"""CLI smoke tests."""

import pytest


@pytest.mark.parametrize("ext", ("dat", "plt"))
def test_dat(script_runner, ext):
    """Check that the quick-plot CLI succeeds for both file types."""
    ret = script_runner.run(["bat-quick", "x=0_var_2_n00000000." + ext], cwd="examples")
    assert ret.success

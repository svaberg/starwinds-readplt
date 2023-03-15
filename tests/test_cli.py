import numpy as np
import matplotlib.pyplot as plt

import pytest

@pytest.mark.parametrize("ext", ("dat", "plt"))
def test_dat(script_runner, ext):
    ret = script_runner.run("sw-quick", "x=0_var_2_n00000000." + ext, cwd="examples")
    assert ret.success

import numpy as np
import matplotlib.pyplot as plt

from starwinds_readplt.cli_plots import quick_plot
from starwinds_readplt.dataset import Dataset
from starwinds_readplt.dataset import triangles

import pytest


def test_dat(script_runner):
    ret = script_runner.run('sw-quick', 'x=0_var_2_n00000000.dat', cwd='examples')
    assert ret.success

def test_plt(script_runner):
    ret = script_runner.run('sw-quick', 'x=0_var_2_n00000000.plt', cwd='examples')
    assert ret.success

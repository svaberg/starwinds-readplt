import logging
try:
    import coloredlogs
except ModuleNotFoundError:
    pass
log = logging.getLogger(__name__)

import argparse
import glob
import re

from slugify import slugify

from my_package.dataset import Dataset, auto_coords, triangles
from my_package.quick_plots import plot

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors

def quick_plot():
    parser = argparse.ArgumentParser(description='Quick plots of 2D SWMF output')
    parser.add_argument('plt_file', type=str, nargs='+',
                        help='Tecplot .plt or .dat files to join, '
                             'or glob pattern expanded by the shell (e.g. y=0*.plt for all the 2D y=0 plots)')
    parser.add_argument('--u_name', dest='u_name', type=str, default=None, help="First  coordinate (e.g. \"X [R]\")")
    parser.add_argument('--v_name', dest='v_name', type=str, default=None, help="Second coordinate (e.g. \"Y [R]\")")
    parser.add_argument('--w_name', dest='w_name', type=str, default="Rho [g/cm^3]", help="Variable to plot (e.g. \"Rho [g/cm^3]\")")
    parser.add_argument('--wscale', dest='wscale', type=str, default="log", help="Variable scale (linear or log)")
    parser.add_argument('-q', '--quiet', dest='log_level', action='store_const',
                        const=logging.WARNING, default=logging.INFO, help='only log warnings and errors')
    parser.add_argument('-v', '--verbose', dest='log_level', action='store_const',
                        const=logging.DEBUG, help='generate and log detailed debug output')

    args = parser.parse_args()

    logging.getLogger(__package__).setLevel(args.log_level)  # Set for entire package.
    try:
        coloredlogs.install(args.log_level, logger=log)
        log.info("Using colorful log messages!")
    except ModuleNotFoundError:
        pass

    plt_filenames = args.plt_file

    # Check for no files found.
    if len(plt_filenames) == 1:
        if '*' in plt_filenames[0] or '?' in plt_filenames[0]:
            # This means that the shell did not expand the glob, which means that no files were found.
            log.error("No files found matching pattern '%s'. Exiting." % plt_filenames[0])
            exit(1)
    
    u_name = args.u_name
    v_name = args.v_name
    w_name = args.w_name

    png_filenames = [slugify(f"ql-{f}-{w_name}") + ".png" for f in plt_filenames]
    for file, pngfile in zip(plt_filenames, png_filenames):
        theplot(file, pngfile, args.u_name, args.v_name, args.w_name, args.wscale)
    
def theplot(file, pngfile, u_name, v_name, w_name, wscale):

    log.info(f"Opening file {file}")
    ds = Dataset.from_file(file)

    if u_name is None and v_name is None:
        u_name, v_name = auto_coords(ds)

    tris = triangles(ds, u_name, v_name)

    fig, ax = plt.subplots()

    w_var = ds.variable(w_name)

    if wscale == "log":
        assert np.log10(10) == 1
        w_var = np.log10(w_var)
        w_name = "log10 " + w_name

    img = ax.tricontourf(tris, w_var, levels=100)
    cax = plt.colorbar(img)

    ax.set_title(ds.title + "\n" + str(file) + " " + ds.zone)
    ax.set_xlabel(u_name)
    ax.set_ylabel(v_name)
    ax.set_aspect("equal")
    cax.set_label(w_name)
    log.info(f"Saving figure {pngfile}.")
    plt.savefig(pngfile)
    plt.close()

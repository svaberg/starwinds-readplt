import logging

log = logging.getLogger(__name__)
import argparse

from slugify import slugify

try:
    import coloredlogs
except ModuleNotFoundError:
    pass

from . import basicplot

plot_callback = basicplot.plot
try:
    from . import fancyplot

    plot_callback = fancyplot.plot
except ImportError:
    pass


def quick_plot():
    parser = argparse.ArgumentParser(description="Quick plots of 2D SWMF output")
    parser.add_argument(
        "plt_file",
        type=str,
        nargs="+",
        help="Tecplot .plt or .dat files to join, "
        "or glob pattern expanded by the shell (e.g. y=0*.plt for all the 2D y=0 plots)",
    )
    parser.add_argument(
        "--u_name",
        dest="u_name",
        type=str,
        default=None,
        help='First  coordinate (e.g. "X [R]")',
    )
    parser.add_argument(
        "--v_name",
        dest="v_name",
        type=str,
        default=None,
        help='Second coordinate (e.g. "Y [R]")',
    )
    parser.add_argument(
        "--w_name",
        dest="w_name",
        type=str,
        default="Rho [g/cm^3]",
        help='Variable to plot (e.g. "Rho [g/cm^3]")',
    )
    parser.add_argument(
        "--wscale",
        dest="wscale",
        type=str,
        default="log",
        help="Variable scale (linear or log)",
    )
    parser.add_argument(
        "-q",
        "--quiet",
        dest="log_level",
        action="store_const",
        const=logging.WARNING,
        default=logging.INFO,
        help="only log warnings and errors",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        dest="log_level",
        action="store_const",
        const=logging.DEBUG,
        help="generate and log detailed debug output",
    )

    args = parser.parse_args()

    logging.getLogger(__package__).setLevel(args.log_level)
    logging.basicConfig(
        format="%(asctime)s %(name)s %(levelname)s: %(message)s", level=args.log_level
    )
    try:
        coloredlogs.install(args.log_level, logger=log)
        log.info("Using colorful log messages!")
    except NameError:
        pass

    plt_filenames = args.plt_file

    # Check for no files found.
    if len(plt_filenames) == 1:
        if "*" in plt_filenames[0] or "?" in plt_filenames[0]:
            # This means that the shell did not expand the glob, which means that no files were found.
            log.error(
                "No files found matching pattern '%s'. Exiting." % plt_filenames[0]
            )
            exit(1)

    png_filenames = [slugify(f"ql-{f}-{args.w_name}") + ".png" for f in plt_filenames]
    for file, png_file in zip(plt_filenames, png_filenames):
        plot_callback(file, png_file, args.u_name, args.v_name, args.w_name, args.wscale)

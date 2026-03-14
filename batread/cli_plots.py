"""CLI entry point for generating quick diagnostic plots."""

import os
import logging
import argparse
import re

try:
    import coloredlogs
except ModuleNotFoundError:
    pass

log = logging.getLogger(__name__)


def quick_plot():
    """Parse CLI args and generate one plot per input file."""
    parser = argparse.ArgumentParser(
        description="Quick plots of 2D SWMF/BATSRUS output"
    )
    parser.add_argument(
        "plt_file",
        type=str,
        nargs="+",
        help="SWMF/BATSRUS 2D slice output file(s) in .plt or .dat format, "
        "or glob pattern of such files expanded by the shell (e.g. y=0*.plt for all the 2D y=0 plots)",
    )
    parser.add_argument(
        "--u_name",
        dest="u_name",
        type=str,
        default=None,
        help='Coordinate variable to use on the plot x axis (e.g. "X [R]")',
    )
    parser.add_argument(
        "--v_name",
        dest="v_name",
        type=str,
        default=None,
        help='Coordinate variable to use on the plot y axis (e.g. "Y [R]")',
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
        help="Only log warnings and errors",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        dest="log_level",
        action="store_const",
        const=logging.DEBUG,
        help="Generate and log detailed debug output",
    )
    parser.add_argument(
        "--noclobber",
        dest="noclobber",
        action="store_true",
        help="Do not overwrite existing files",
    )
    parser.add_argument(
        "--identifier",
        dest="identifier",
        type=str,
        default=None,
        help="Optional identifier string to add to the plot title",
    )

    args = parser.parse_args()

    logging.getLogger(__package__).setLevel(args.log_level)
    logging.basicConfig(format="%(levelname)s: %(message)s", level=args.log_level)
    try:
        coloredlogs.DEFAULT_LEVEL_STYLES["info"] = {"color": "green"}
        coloredlogs.DEFAULT_LOG_FORMAT = "%(message)s"
        coloredlogs.install(args.log_level, logger=log)
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

    try:
        from . import fancyplot
    except ImportError:
        try:
            from . import basicplot
        except ModuleNotFoundError as exc:
            if exc.name == "matplotlib":
                raise SystemExit(
                    "The matplotlib package is required for plotting. "
                    "Install matplotlib in your environment, or run: "
                    "pip install batread[graphics]"
                ) from exc
            raise
        plot_callback = basicplot.plot
    else:
        plot_callback = fancyplot.plot

    png_filenames = [
        re.sub(r"[^a-z0-9]+", "-", f"ql-{file}-{args.w_name}".lower()).strip("-")
        + ".png"
        for file in plt_filenames
    ]
    for file, png_file in zip(plt_filenames, png_filenames):
        if args.noclobber and os.path.exists(png_file):
            log.warning("Skipping existing file %s" % png_file)
            continue
        plot_callback(
            file,
            png_file,
            args.u_name,
            args.v_name,
            args.w_name,
            args.wscale,
            args.identifier,
        )

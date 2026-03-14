# Release Checklist

This project is intended for PyPI distribution. Only committed state should be considered shippable.

## Completed

1. Keep missing `TITLE=` represented as `None` from `batread/read_dat.py`.
2. Make plotting robust to missing titles in `batread/basicplot.py`.
3. Add a CLI smoke test for plotting a title-less `.dat` file in `tests/test_cli.py`.
4. Replace format-validation `assert` statements in `batread/read_plt.py` with explicit exceptions.
5. Add PyPI-facing metadata to `pyproject.toml`.
6. Update the README links to use the `batread` repository.
7. Update the GitHub workflow coverage target to use `batread`.

## Repository Cleanup

1. Decide whether `batread/read_plt_ondemand.py` should ship.
   It is explicitly experimental and incomplete; either remove it from the published surface or finish it.

## Release Verification

1. Build the sdist and wheel.
   `python -m build`
2. Check the built metadata.
   `twine check dist/*`
3. Install the built wheel in a clean environment and run `pytest`.
4. Smoke-test `bat-quick` from the installed artifact, not from the source tree.

## Nice To Have

1. Update the README installation section to reflect the actual published package name and extras.
2. Add a short release workflow for tagging and uploading to PyPI/TestPyPI.

# Release Checklist

This project is intended for PyPI distribution. Only committed state should be considered shippable.

## Blockers Before Release

1. Replace format-validation `assert` statements in `batread/read_plt.py` with explicit exceptions.
   A public parser should fail with clear errors even when Python assertions are disabled.

## Completed

1. Keep missing `TITLE=` represented as `None` from `batread/read_dat.py`.
2. Make plotting robust to missing titles in `batread/basicplot.py`.
3. Add a CLI smoke test for plotting a title-less `.dat` file in `tests/test_cli.py`.

## Packaging Metadata

1. Add `readme` metadata in `pyproject.toml`.
2. Add `requires-python` in `pyproject.toml`.
3. Add author and/or maintainer metadata in `pyproject.toml`.
4. Add project URLs in `pyproject.toml`.
   At minimum: repository, issues, and homepage if distinct.
5. Add classifiers in `pyproject.toml`.
6. Avoid version drift between `pyproject.toml` and `batread/__init__.py`.

## Repository Cleanup

1. Update rename leftovers in `README.md`.
   The badges and links still point to `starwinds-readplt`.
2. Update rename leftovers in `.github/workflows/python-package.yml`.
   Coverage is still collected against `starwinds_readplt`.
3. Decide whether `batread/read_plt_ondemand.py` should ship.
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

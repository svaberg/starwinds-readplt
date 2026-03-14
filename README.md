[![Python package](https://github.com/svaberg/batread/actions/workflows/python-package.yml/badge.svg)](https://github.com/svaberg/batread/actions/workflows/python-package.yml)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/6236f7130d7f4b0caab5ee221430e74b)](https://app.codacy.com/gh/svaberg/batread/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=svaberg/batread&amp;utm_campaign=Badge_Grade)
[![Codacy Badge](https://app.codacy.com/project/badge/Coverage/6236f7130d7f4b0caab5ee221430e74b)](https://app.codacy.com/gh/svaberg/batread/dashboard?utm_source=github.com&utm_medium=referral&utm_content=svaberg/batread&utm_campaign=Badge_Coverage)
[![DOI](https://zenodo.org/badge/550311707.svg)](https://zenodo.org/badge/latestdoi/550311707)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


The `batread` project is a Python library for reading
[SWMF/BATSRUS](https://clasp.engin.umich.edu/research/theory-computational-methods/space-weather-modeling-framework/)
output and related Tecplot ASCII `.dat` and binary `.plt` datasets. The project also includes a use case in the form of a quicklook command, `bat-quick`, for visualising two-dimensional SWMF/BATSRUS output.

## Installation
After cloning this repository, the project may be installed with `pip` in the regular way:
```bash
cd <project>
pip install .
```

This installs the reader functionality only. To use the quicklook plotting command, install the graphics extra:
```bash
pip install .[graphics]
```

## Python code to access file data
This code reads a dataset named `<file>` and stores the dataset variable named `Rho [g/cm^3]` in a local variable named `density_g_cm3`.
```python
from batread import Dataset
ds = Dataset.from_file('<file>')
print(ds)
density_g_cm3 = ds('Rho [g/cm^3]')
```

## Running the quicklook command
A simple 'quicklook' shell command is included which permits plotting of two-dimensional slices of the SWMF/BATSRUS results. Irregularly gridded data is accepted. The quicklook command uses the plot function in `basicplot.py` but this may be extended by the user.

The quicklook command requires the graphics extra:
```bash
pip install .[graphics]
```

To create a quicklook `.png` file from the included file `examples/x=0_var_2_n00000000.plt`
run
```bash
cd examples
bat-quick x=0_var_2_n00000000.plt
```
This will create a file named `ql-x-0-var-2-n00000000-plt-rho-g-cm-3.png`; the name comprises the prefix `ql`, the file name, and the name of the plotted variable. Non-alphanumeric characters are normalised to dashes in the output file name.

A wildcard pattern may be used; in this case one `.png` file is created for each file matching the wildcard pattern:

```bash
bat-quick x*.plt
```

## Development and testing

To install the project in editable mode and enable testing do

```bash
cd <project>
pip install --editable .[tests]
```

Now it is possible to run the test suite by typing

```bash
pytest
```

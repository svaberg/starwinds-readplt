[![Python package](https://github.com/svaberg/starwinds-readplt/actions/workflows/python-package.yml/badge.svg)](https://github.com/svaberg/starwinds-readplt/actions/workflows/python-package.yml)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/6236f7130d7f4b0caab5ee221430e74b)](https://www.codacy.com/gh/svaberg/starwinds-readplt/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=svaberg/starwinds-readplt&amp;utm_campaign=Badge_Grade)
[![Codacy Badge](https://app.codacy.com/project/badge/Coverage/6236f7130d7f4b0caab5ee221430e74b)](https://www.codacy.com/gh/svaberg/starwinds-readplt/dashboard?utm_source=github.com&utm_medium=referral&utm_content=svaberg/starwinds-readplt&utm_campaign=Badge_Coverage)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

The `readplt` project is a Python library for reading and parsing 
[SWMF/BATSRUS](https://clasp.engin.umich.edu/research/theory-computational-methods/space-weather-modeling-framework/)
output files in `.dat` and `.plt` format. The library may aso be able to read other `.plt` files but only a core subset of the `.plt` format specification is supported. The project also includes an use case in the form of a 'quicklook' command `sw-quick` that can visualise two-dimensional SWMF/BATSRUS output.


## Installation
After cloning this repository, the project may be installed with `pip` in the regular way:
```bash
cd <project>
pip install .
```

## Python code to access file data
This code reads a dataset named `<file>` and stores the dataset variable named `Rho [g/cm^3]` in a local variable named `density_g_cm3`.
```python
from starwinds_readplt.dataset import Dataset
ds = Dataset('<file>')
print(ds)
density_g_cm3 = ds.variable('Rho [g/cm^3]')
```

## Running the quicklook command
A simple 'quicklook' shell command is included which permits plotting of two-dimensional slices of the SWMF/BATSRUS results. Irregularly gridded data is accepted. The quicklook command uses the plot function in `basicplot.py` but this may be extended by the user.

To create a quicklook `.png` file from the included file `examples/x=0_var_2_n00000000.plt`
run
```bash
cd examples
sw-quick x=0_var_2_n00000000.plt
```
This will create a file named `ql-x-0-var-2-n00000000-plt-rho-g-cm-3.png`; the name comprises the prefix `ql`, the file name, and the name of the plotted variable. The name is sanitised using [`slugify`](https://pypi.org/project/python-slugify/) to replace spaces and other problematic characters in the output file name with dashes.

A wildcard pattern may be used; in this case one `.png` file is created for each file matching the wildcard pattern:

```bash
sw-quick x*.plt
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

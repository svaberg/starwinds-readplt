[![Python package](https://github.com/svaberg/starwinds-readplt/actions/workflows/python-package.yml/badge.svg)](https://github.com/svaberg/starwinds-readplt/actions/workflows/python-package.yml)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/6236f7130d7f4b0caab5ee221430e74b)](https://www.codacy.com/gh/svaberg/starwinds-readplt/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=svaberg/starwinds-readplt&amp;utm_campaign=Badge_Grade)
[![Codacy Badge](https://app.codacy.com/project/badge/Coverage/6236f7130d7f4b0caab5ee221430e74b)](https://www.codacy.com/gh/svaberg/starwinds-readplt/dashboard?utm_source=github.com&utm_medium=referral&utm_content=svaberg/starwinds-readplt&utm_campaign=Badge_Coverage)

The `readplt` project can read and parse SWMF/BATSRUS output files in `.dat` and `.plt` format. It may aso be able to read other `.plt` files but only a small subset of the `.plt` format specification is supported.

## Installation

To install 

```bash
cd <project>
pip install .
```

## Running the quick look

To create a single example `.png` file

```bash
sw-quick x=0_var_2_n00000000.plt
```

or several files based on a wildcard pattern

```bash
sw-quick x*.plt
```

## Python code to access file data
This code reads a dataset named `<file>` and stores the dataset variable named `Rho [g/cm^3]` in a local variable named `RHO`.
```python
from starwinds_readplt.dataset import Dataset
ds = Dataset('<file>')
print(ds)
RHO = ds.variable('Rho [g/cm^3]')
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

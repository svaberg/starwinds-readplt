# batread

`batread` is a Python library for reading SWMF/BATSRUS output and related
Tecplot ASCII `.dat` and binary `.plt` datasets.

The package also provides a quicklook command, `bat-quick`, for visualising
two-dimensional SWMF/BATSRUS output.

## Installation

Install the reader with:

```bash
pip install batread
```

To use the quicklook plotting command, install the graphics extra:

```bash
pip install "batread[graphics]"
```

## Python usage

```python
from batread import Dataset

ds = Dataset.from_file("your-file.plt")
print(ds)

rho = ds["Rho [g/cm^3]"]
xyz = ds[["X [R]", "Y [R]", "Z [R]"]]
```

## Quicklook usage

After installing the graphics extra, run:

```bash
bat-quick your-file.plt
```

This creates a `.png` quicklook image for the selected variable.

## Example data

Example files and repository-oriented examples live in the GitHub repository.
They are not included in the PyPI wheel.

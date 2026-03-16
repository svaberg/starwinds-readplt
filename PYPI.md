The `batread` project is a Python library for reading
[SWMF/BATSRUS](https://clasp.engin.umich.edu/research/theory-computational-methods/space-weather-modeling-framework/)
output and related Tecplot ASCII `.dat` and binary `.plt` datasets. The project also includes a use case in the form of a quicklook command, `bat-quick`, for visualising two-dimensional SWMF/BATSRUS output.

## Installation
The project may be installed with `pip` in the regular way:
```bash
pip install batread
```

## Python code to access file data
This code reads a dataset named `<file>` and stores the dataset variable named `Rho [g/cm^3]` in a local variable named `density_g_cm3`.
```python
from batread import Dataset
ds = Dataset.from_file('<file>')
print(ds)
density_g_cm3 = ds['Rho [g/cm^3]']
```

## Running the quicklook command
A simple 'quicklook' shell command is included which permits plotting of two-dimensional slices of the SWMF/BATSRUS results. Irregularly gridded data is accepted. The quicklook command uses the plot function in `basicplot.py` but this may be extended by the user.

The quicklook command requires `matplotlib`.

To create a quicklook `.png` file from a `.plt` file
run
```bash
bat-quick <file>
```
This will create a `.png` file; the file name comprises the prefix `ql`, the file name, and the name of the plotted variable. Non-alphanumeric characters are normalised to dashes in the output file name.

A wildcard pattern may be used; in this case one `.png` file is created for each file matching the wildcard pattern:

```bash
bat-quick x*.plt
```

Further code examples and data files are available in the [GitHub repository](https://github.com/svaberg/batread/tree/master/sample_data).

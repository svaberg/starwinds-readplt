[![Python package](https://github.com/svaberg/starwinds-readplt/actions/workflows/python-package.yml/badge.svg)](https://github.com/svaberg/starwinds-readplt/actions/workflows/python-package.yml)

## Installation
To install 
```
cd <project>
pip install .
```

## Running the quick look
To create a single example png
```
sw-quick x=0_var_2_n00000000.plt
```
or several png files
```
sw-quick x*.plt
```

## Development and testing
To install the project in editable mode and enable testing do
```
cd <project>
pip install --editable .[tests]
```
Now it is possible to run the test suite by typing
```
pytest
```

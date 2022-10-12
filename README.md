[![Python package](https://github.com/svaberg/starwinds-readplt/actions/workflows/python-package.yml/badge.svg)](https://github.com/svaberg/starwinds-readplt/actions/workflows/python-package.yml)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/6236f7130d7f4b0caab5ee221430e74b)](https://www.codacy.com/gh/svaberg/starwinds-readplt/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=svaberg/starwinds-readplt&amp;utm_campaign=Badge_Grade)
[![Codacy Badge](https://app.codacy.com/project/badge/Coverage/6236f7130d7f4b0caab5ee221430e74b)](https://www.codacy.com/gh/svaberg/starwinds-readplt/dashboard?utm_source=github.com&utm_medium=referral&utm_content=svaberg/starwinds-readplt&utm_campaign=Badge_Coverage)

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

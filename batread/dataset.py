"""Container type and loaders for BATSRUS datasets."""

from batread.read_dat import read_dat
from batread.read_plt import read_plt


class Dataset:
    """In-memory dataset with points, connectivity, and metadata."""

    def __init__(self, points, corners, aux, title, variables, zone):
        """Store arrays and metadata for one parsed dataset."""
        self.points = points
        self.corners = corners
        self.aux = aux
        self.title = title
        self.variables = variables
        self.zone = zone

    def __str__(self):
        """Return a compact human-readable summary."""
        s = [
            f"Title:     '{self.title}'",
            f"Zone:      '{self.zone}'",
            f"Variables: {len(self.variables)}",
            f"Shape:     {self.points.shape}",
            f"Variables: {self.variables}.",
        ]
        return "\n".join(s)

    @classmethod
    def from_file(cls, file):
        """Load a dataset from .dat or .plt by extension."""
        if file.split(".")[-1] == "dat":
            return cls.from_dat(file)
        elif file.split(".")[-1] == "plt":
            return cls.from_plt(file)
        else:
            raise ValueError(f"Unknown extension for file {file}.")

    @classmethod
    def from_dat(cls, file):
        """Load a dataset from an ASCII .dat file."""
        points, corners, aux, title, variables, zone = read_dat(file)
        return cls(points, corners, aux, title, variables, zone)

    @classmethod
    def from_plt(cls, file):
        """Load a dataset from a binary .plt file."""
        points, corners, aux, title, variables, zone = read_plt(file)
        return cls(points, corners, aux, title, variables, zone)

    def _variable(self, index_or_name):
        """Return one variable, slice, or list of variables.

        Accepted keys are integer-like indices, exact variable names,
        integer slices, and lists/tuples of integer-like indices or names.
        """
        if isinstance(index_or_name, slice):
            return self.points[..., index_or_name]

        if isinstance(index_or_name, (list, tuple)):
            return self.points[
                ..., [self._variable_index(key) for key in index_or_name]
            ]

        return self.points[..., self._variable_index(index_or_name)]

    def _variable_index(self, index_or_name):
        """Return one variable index by integer-like value or exact name."""
        try:
            index = int(index_or_name)
            return index
        except ValueError:
            pass

        try:
            return self.variables.index(index_or_name)
        except ValueError:
            pass

        raise IndexError(
            f"Variable '{index_or_name}' not in dataset. Available variables are {self.variables}."
        )

    def __getitem__(self, index_or_name):
        """Return one variable, slice, or list of variables."""
        return self._variable(index_or_name)

    def span(self, index_or_name):
        """Calculate the span of a variable; used for coordinate centering"""
        var = self._variable(index_or_name)
        return var.min(), var.max()

    def center(self, index_or_name):
        """Calculate the center value of a variable; used for coordinate centering"""
        var = self._variable(index_or_name)
        return (var.min() + var.max()) / 2

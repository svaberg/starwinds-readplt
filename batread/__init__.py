"""Public package interface for batread."""

from importlib.metadata import version

from batread.dataset import Dataset

__version__ = version("batread")

__all__ = ["Dataset", "__version__"]

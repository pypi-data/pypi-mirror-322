"""
SynthGen - A Python library for generating synthetic datasets
"""

from .core import SynthGen
from .tabular import TabularGenerator

__version__ = "0.1.0"
__all__ = ["SynthGen", "TabularGenerator"]
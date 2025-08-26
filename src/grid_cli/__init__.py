"""
Grid-Cell Neighborhoods: Count cells within Manhattan distance of positive values.

This package provides classes to work with 2D grids and calculate neighborhoods
based on Manhattan distance.
"""

from .neighbor_searches import BruteForce
from .Grid import Grid
from .GridCell import GridCell

__all__ = ['Grid', 'GridCell']

import math
from numbers import Number
from typing import Any, Sequence

class GridCell:
    """
    Represents a cell in a 2D grid with row/column coordinates. The value that
    the cell is holding can be any object. For type-specific functionality,
    derive a new class.
    
    Provides intuitive math operators for common operations
    """
    def __init__(self, row: int, col: int, value: Any):

        """
        Initialize a grid cell with coordinates.
        
        Args:
            row: Row coordinate (0-based)
            col: Column coordinate (0-based)
        """
        self._validate_cell(row, col)
        self.row = row
        self.col = col
        self.value = value
    
    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"GridCell({self.row}, {self.col}, {self.value})"

    def __eq__(self, other) -> bool:
        """Check equality with another GridCell."""
        if isinstance(other, GridCell):
            return self.row == other.row and self.col == other.col
        elif isinstance(other, Sequence) and len(other) == 2:
            return self.row == other[0] and self.col == other[1]
        else:
            return False
    
    def __hash__(self) -> int:
        """Unique cell is defined by coordinates only to avoid cases where
        the cell's value isn't hashable."""
        return hash((self.row, self.col))

    def __add__(self, other: "GridCell | tuple[int, int]"):
        other_row, other_col = self.__get_row_col(other)
        return type(self)(self.row + other_row, self.col + other_col, self.value)

    def __iadd__(self, other: "GridCell | tuple[int, int]"):
        other_row, other_col = self.__get_row_col(other)
        self.row += other_row
        self.col += other_col
        return self

    def __sub__(self, other: "GridCell | tuple[int, int]"):
        return type(self)(self.row - other.row, self.col - other.col, self.value)

    def __isub__(self, other: "GridCell | tuple[int, int]"):
        other_row, other_col = self.__get_row_col(other)
        self.row -= other_row
        self.col -= other_col
        return self

    def __abs__(self):
        return type(self)(abs(self.row), abs(self.col), self.value)

    def __gt__(self, other: "GridCell | int"):
        return self.value > self.__get_value(other)

    def __ge__(self, other: "GridCell | int"):
        return self.value >= self.__get_value(other)

    def __lt__(self, other: "GridCell | int"):
        return self.value < self.__get_value(other)

    def __le__(self, other: "GridCell | int"):
        return self.value <= self.__get_value(other)

    @property
    def coords(self) -> Sequence[int]:
        return self.row, self.col

    def manhattan_distance(self, other: 'GridCell', wrap_row_at=None, wrap_col_at=None) -> int:
        """
        Calculate Manhattan distance to another GridCell.

        https://en.wikipedia.org/wiki/Taxicab_geometry
        """
        dist = self.__get_abs_delta(other, wrap_row_at, wrap_col_at)
        return dist.row + dist.col

    def chebyshev_distance(self, other: 'GridCell', wrap_row_at=None, wrap_col_at=None) -> int:
        dist = self.__get_abs_delta(other, wrap_row_at, wrap_col_at)
        return max(dist.row, dist.col)

    def copy(self, value=None):
        # TODO: make sure to deep copy `value` in case its an object
        return type(self)(self.row, self.col, self.value if value is None else value)

    def _validate_cell(self, row, col):
        # allow indices to be negative as a result of subtract operation
        # TODO: Maybe derive new class that bypasses index validation, but inherits the rest of the functionality?
        # if row < 0 or col < 0:
        #     raise ValueError(f"Row({row}) and column({col}) must be non-negative")
        pass

    def __get_row_col(self, other: "GridCell | Sequence[int, int]") -> tuple[int, int]:
        return (other.row, other.col) if isinstance(other, GridCell) else other

    def __get_value(self, other: "GridCell | Number") -> Number:
        return other.value if isinstance(other, GridCell) else other

    def __get_abs_delta(self, other: "GridCell", wrap_row_at=None, wrap_col_at=None) -> "GridCell":
        dist = abs(self - other)
        if wrap_row_at is not None:
            dist.row = min(dist.row, wrap_row_at - dist.row)
        if wrap_col_at is not None:
            dist.col = min(dist.col, wrap_col_at - dist.col)
        return dist

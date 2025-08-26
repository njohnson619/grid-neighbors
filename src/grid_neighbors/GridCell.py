from typing import Any

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
        elif isinstance(other, tuple) and len(other) == 2:
            return self.row == other[0] and self.col == other[1]
        else:
            return False
    
    def __hash__(self) -> int:
        """Unique cell is defined by coordinates only to avoid cases where
        the cell's value isn't hashable."""
        return hash((self.row, self.col))

    def __add__(self, other):
        return GridCell(self.row + other.row, self.col + other.col, self.value)

    def __sub__(self, other):
        return GridCell(self.row - other.row, self.col - other.col, self.value)

    def manhattan_distance(self, other: 'GridCell') -> int:
        """
        Calculate Manhattan distance to another GridCell.

        https://en.wikipedia.org/wiki/Taxicab_geometry
        """
        delta = self - other
        return abs(delta.row) + abs(delta.col)

    def copy(self, value=None):
        # TODO: make sure to deep copy `value` in case its an object
        return type(self)(self.row, self.col, self.value if value is None else value)

    def _validate_cell(self, row, col):
        # allow indices to be negative as a result of subtract operation
        # TODO: Maybe derive new class that bypasses index validation, but inherits the rest of the functionality?
        # if row < 0 or col < 0:
        #     raise ValueError(f"Row({row}) and column({col}) must be non-negative")
        pass

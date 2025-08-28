import logging
from abc import ABC, abstractmethod
from typing import Sequence

from .Grid import Grid, Matrix
from .GridCell import GridCell
from .Logger import create_logger, set_global_log_level

logger = create_logger(__name__)


class SearchBase(ABC):
    @classmethod
    def create_result(cls, neighbors: Sequence[GridCell]) -> dict:
        # autogen'd FE code expects a different format
        fe_neighbors = [
            {
                'row': neighbor.row,
                'col': neighbor.col,
                'distance': neighbor.value,
                'is_positive': neighbor.value == 0
            }
            for neighbor in neighbors
        ]
        pos_cells = [
            {
                'row': fe_neighbor['row'],
                'col': fe_neighbor['col'],
            }
            for  fe_neighbor in fe_neighbors
            if fe_neighbor["is_positive"]
        ]
        return {
            # positive cells are included in the count per task description
            "count": len(neighbors),
            "neighbors": fe_neighbors,
            "positive_cells": pos_cells,
        }

    def __init__(self, data: Matrix | Grid, max_distance: int, wrap_rows=False, wrap_cols=False):
        self.grid = data if isinstance(data, Grid) else Grid(data)
        if max_distance < 0:
            raise ValueError(f"Max distance must be non-negative. Received {max_distance}")
        self.max_distance = max_distance
        self.wrap_rows = wrap_rows
        self.wrap_cols = wrap_cols

    @abstractmethod
    def find_neighbors(self) -> Sequence[GridCell]:
        pass


class BreadthFirstSearch(SearchBase):
    def find_neighbors(self) -> Sequence[GridCell]:
        return []


class BruteForceSearch(SearchBase):
    def find_neighbors(self):
        # save locally, for perf
        num_rows, num_cols = self.grid.shape
        src_cells = self.grid.positive_cells
        if not src_cells:
            return []

        # unique list of cells in the neighborhood (ignoring value)
        neighbors = set()

        # iterate every single cell in the grid (brute force)
        for cell in self.grid:
            # calculate distance to all source cells (considering possible index wrapping in
            # both dimensions) and save the distance to the closest one
            min_distance = min(
                [
                    src_cell.manhattan_distance(
                        cell,
                        wrap_row_at=self.grid.num_rows if self.wrap_rows else None,
                        wrap_col_at=self.grid.num_cols if self.wrap_cols else None
                    )
                    for src_cell in src_cells
                ]
            )
            # if closest source cell is in range, then current cell is a neighbor
            # of at least one of the sources and should be included
            if min_distance <= self.max_distance:
                # copy cell to preserve relative distance to the nearest source
                new_neighbor = cell.copy(value=min_distance)
                curr_ct = len(neighbors)
                neighbors.add(new_neighbor)
                if len(neighbors) == curr_ct:
                    logger.debug(f"\tSkipping duplicate neighbor: {new_neighbor}")

        return neighbors














import logging
from typing import Sequence

from .Grid import Grid, Matrix
from .GridCell import GridCell
from .Logger import create_logger, set_global_log_level

logger = create_logger(__name__)

# usually log level is defined in environment
set_global_log_level(logging.DEBUG)

class BruteForce:
    def __init__(self, data: Matrix | Grid, max_distance: int, wrap_rows=False, wrap_cols=False):
        self.grid = data if isinstance(data, Grid) else Grid(data)
        if max_distance < 0:
            raise ValueError(f"Max distance must be non-negative. Received {max_distance}")
        self.max_distance = max_distance
        self.wrap_rows = wrap_rows
        self.wrap_cols = wrap_cols

    def find_neighbors(self):
        # save locally, for perf
        num_rows, num_cols = self.grid.shape
        src_cells = self.grid.positive_cells
        if not src_cells:
            return self.create_result([], [])

        # unique list of cells in the neighborhood (ignoring value)
        neighbors = set()

        # iterate every single cell in the grid (brute force)
        for cell in self.grid:
            # sort source cells by distance to current cell to determine if it's a neighbor
            min_distance = min([src_cell.manhattan_distance(cell) for src_cell in src_cells])

            if min_distance <= self.max_distance:
                # copy cell to preserve relative distance to the nearest source
                new_neighbor = cell.copy(value=min_distance)
                curr_ct = len(neighbors)
                neighbors.add(new_neighbor)
                if len(neighbors) == curr_ct:
                    logger.debug(f"\tSkipping duplicate neighbor: {new_neighbor}")
            # else:
            #     logger.debug(f"\tCurrent cell not in neighborhood, dist: {min_distance}")

        return self.create_result(list(neighbors), src_cells)


    def create_result(self, neighbors: Sequence[GridCell], source_cells: Sequence[GridCell]) -> dict:
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
        # for n in fe_neighbors:
        #     logger.debug(f"{n.get('distance')}, {n=}")
        p_cells = [
            {
                'row': s_cell.row,
                'col': s_cell.col,
            }
            for s_cell in source_cells
        ]
        return {
            # positive cells are included in the count per task description
            "count": len(neighbors),
            "neighbors": fe_neighbors,
            "positive_cells": p_cells,
            # repeat back request details to frontend as a double check
            "max_distance": self.max_distance,
            "wrap_rows": self.wrap_rows,
            "wrap_cols": self.wrap_cols,
        }













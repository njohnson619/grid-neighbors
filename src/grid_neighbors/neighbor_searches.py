import heapq
import logging
from abc import ABC, abstractmethod
from collections import deque
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
        self.grid = data if isinstance(data, Grid) else Grid(data, wrap_rows, wrap_cols)
        # if grid was specified, make sure it's consistent with the parameters
        self.grid.wrap_rows = wrap_rows
        self.grid.wrap_cols = wrap_cols
        if max_distance < 0:
            raise ValueError(f"Max distance must be non-negative. Received {max_distance}")
        self.max_distance = max_distance

    @abstractmethod
    def find_neighbors(self) -> Sequence[GridCell]:
        pass


class BreadthFirstSearch(SearchBase):
    """
    Multi-source Breadth-First Search (BFS) algorithm.

    Unweighted graph implemented with Python's deque data structure.

    A graph is built where all positive cells start at the root level and each subsequent level consists of all cells
    1 step further away from their parent (neighbor) cell. This guarantees that each cell in the neighborhood only
    has to be visited once while guaranteeing distance is to the closest positive cell. Once, the graph has the same number
    of levels as the specified distance value, any remaining unvisited cells can be skipped.  Implemented with Python's
    deque data structure.
    """
    def find_neighbors(self) -> Sequence[GridCell]:
        src_cells = self.grid.positive_cells
        if not src_cells:
            return []

        # initialize source cells as starting points with distances of 0
        for cell in src_cells:
            cell.value = 0

        # using a set allows for constant-time lookups of presence for already visited cells.
        # set is initialized with source cells because they're part of the neighborhood as well.
        neighborhood = set(src_cells)
        bfs_queue = deque(src_cells, self.grid.num_cells)
        while bfs_queue:
            curr_cell = bfs_queue.popleft()
            if curr_cell.value >= self.max_distance:
                continue
            neighbors = self.grid.get_immediate_neighbors(curr_cell)
            for new_neighbor in neighbors:
                # can safely ignore neighbors that have already been visited
                if new_neighbor not in neighborhood:
                    # distance is set here because `value` is being overloaded and the `get_immediate_neighbors`
                    # method doesn't know in what context its being called to set itself
                    new_neighbor.value = curr_cell.value + 1
                    # add to the neighborhood and queue at next level to process its own neighbors
                    neighborhood.add(new_neighbor)
                    bfs_queue.append(new_neighbor)

        return list(neighborhood)


class BruteForceSearch(SearchBase):
    def find_neighbors(self) -> Sequence[GridCell]:
        # save locally, for perf
        num_rows, num_cols = self.grid.shape
        src_cells = self.grid.positive_cells
        if not src_cells:
            return []

        # unique list of cells in the neighborhood (ignoring value)
        neighbors = set()

        # iterate every single cell in the grid against every source cell (brute force)
        for cell in self.grid:
            dists = []
            for src_cell in src_cells:
                # calculate distance to all source cells (considering possible index wrapping in
                # both dimensions) and save the distance to the closest one
                dist_func = src_cell.chebyshev_distance if self.grid.distance_type == "chebyshev" else src_cell.manhattan_distance
                dists.append(
                    dist_func(
                        cell,
                        wrap_row_at=num_rows if self.grid.wrap_rows else None,
                        wrap_col_at=num_cols if self.grid.wrap_cols else None
                    )
                )
            min_distance = min(dists)
            # if closest source cell is in range, then current cell is a neighbor
            # of at least one of the sources and should be included
            if min_distance <= self.max_distance:
                # copy cell to preserve relative distance to the nearest source
                new_neighbor = cell.copy(value=min_distance)
                curr_ct = len(neighbors)
                neighbors.add(new_neighbor)
                if len(neighbors) == curr_ct:
                    logger.debug(f"\tSkipping duplicate neighbor: {new_neighbor}")

        return list(neighbors)














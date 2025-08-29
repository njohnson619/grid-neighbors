from typing import List, Sequence

from grid_neighbors import Grid, GridCell


def assert_count(neighbors, grid, expected_count, distance, wrap_rows=False, wrap_cols=False):
    assert len(neighbors) == expected_count, plot_ascii_table(grid, distance, neighbors, wrap_rows=wrap_rows, wrap_cols=wrap_cols)

def plot_ascii_table(
    grid: Grid,
    N: int,
    neighbors: Sequence[GridCell],
    show_plus_on_sources: bool = True,
    dot_outside: str = ".",
    wrap_rows: bool = False,
    wrap_cols: bool = False,
) -> str:
    num_rows = grid.num_rows
    if num_rows == 0:
        return "(empty grid)"
    num_cols = grid.num_cols

    # Widths
    row_idx_width = max(len(str(num_rows-1)), 1)
    cell_width = max(len(str(N)), 1)

    # Helpers
    def cell(s: str) -> str:
        return f" {s:>{cell_width}} "

    left_pad = " " * (row_idx_width + 2)  # row index + space + '|'

    def hr() -> str:
        return f"{left_pad}+" + "+".join(["-" * (cell_width + 2) for _ in range(num_cols)]) + "+"

    # Column header
    header_cells = " ".join(cell(str(c)) for c in range(num_cols))
    header = f"{' ' * (row_idx_width + 1)}  {header_cells} "

    n_map = {(c.row, c.col): c.value for c in neighbors}

    # Table header
    tab_hdr = f"{grid}, {N=}, {wrap_rows=}, {wrap_cols=} {len(neighbors)} neighbors"

    # Build table
    lines = [tab_hdr, header, hr()]
    for r in range(num_rows):
        row_label = f"{r:>{row_idx_width}}  |"
        row_cells = []
        for c in range(num_cols):
            neighbor_dist = n_map.get((r, c))
            if neighbor_dist is None:
                new_cell = cell(dot_outside)
            elif neighbor_dist == 0 and show_plus_on_sources:
                new_cell = cell("+")
            else:
                new_cell = cell(str(neighbor_dist))
            row_cells.append(new_cell)

        # safety check: exactly W cells
        if len(row_cells) != num_cols:
            raise RuntimeError(f"Internal error: produced {len(row_cells)} cells for row of width {num_cols}")
        lines.append(row_label + "|".join(row_cells) + "|")
        lines.append(hr())

    return "\n".join(lines)

import secrets
from typing import Any
import click
from .grids import (
    SquareGrid,
    TriangularGrid,
    HexagonalGrid,
)

grid_types: dict[str, Any] = {
    "square": SquareGrid,
    "hexagonal": HexagonalGrid,
    "triangular": TriangularGrid,
    "sqr": SquareGrid,
    "hex": HexagonalGrid,
    "tri": TriangularGrid,
    "s": SquareGrid,
    "h": HexagonalGrid,
    "t": TriangularGrid,
}

grid_types_names = list(grid_types.keys())


class DemoAutomaton:
    name: str = "Demo"

    def __init__(self, grid: list, states: list[int]):
        self.grid = grid
        self.height = len(self.grid)
        self.width = len(self.grid[0])
        self.states = states
        self.step = 0

    def __next__(self):
        for row in range(self.height):
            for col in range(self.width):
                self.grid[row][col] = secrets.choice(self.states)

        self.step += 1


@click.command()
@click.option(
    "-t",
    "--grid-type",
    type=click.Choice(grid_types_names),
    default=grid_types_names[0],
    show_default=True,
    help="Select grid type.",
)
@click.option("-c", "--cols", default=33, show_default=True, help="Set grid number of cols.")
@click.option("-r", "--rows", default=20, show_default=True, help="Set grid number or rows.")
@click.option("-f", "--fps", default=10, show_default=True, help="Set grid number or rows.")
@click.option("-s", "--cell-size", default=48, show_default=True, help="Set grid cell size.")
def main(grid_type: str, rows: int, cols: int, fps: int, cell_size: int):
    colors = [
        "red",
        "green",
        "yellow",
        "blue",
        "cyan",
        "magenta",
        "black",
        "white",
        "gray",
        "darkred",
        "pink",
        "darkgreen",
    ]

    states = list(range(0, len(colors)))

    grid: list[list[int]] = []

    for row in range(rows):
        grid.append([])
        for _ in range(cols):
            grid[row].append(secrets.choice(states))

    automaton = DemoAutomaton(grid=grid, states=states)

    grid_types[grid_type](
        title=automaton.name,
        automaton=automaton,
        tile_size=cell_size,
        fps=fps,
        colors=tuple(colors),
    ).mainloop()


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter

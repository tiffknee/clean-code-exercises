# TODO: refactor & clean up this class.
#  - Familiarize yourself with the code and what it does (it is easiest to read the tests first)
#  - refactor ...
#     - give the functions/variables proper names
#     - make the function bodies more readable
#     - clean up the test code where beneficial
#     - make sure to put each individual change in a small, separate commit
#     - take care that on each commit, all tests pass
from typing import Tuple
from dataclasses import dataclass

@dataclass
class Point:
    x: float
    y: float

class RasterGrid:
    @dataclass
    class Cell:
        _ix: int
        _iy: int

    def __init__(self,
                 origin: Point,
                 size: Tuple[float,float],
                 nx: int,
                 ny: int) -> None:
        self._origin = origin
        self._extent = Point(
            self._origin.x + size[0],
            self._origin.y + size[1]
            )
        self._nx = nx
        self._ny = ny
        self.nc = nx*ny
        self.cells = [
            self.Cell(i, j) for i in range(nx) for j in range(ny)
        ]

    # @property
    # def cells(self) -> List[Cell]:
    #     return [
    #         self.Cell(i, j) for i in range(self._nx) for j in range(self._ny)
    #     ]

    # @property
    # def number_of_cells(self) -> int:
    #     return self._nx*self._ny

    def get_center_coordinates(self, cell: Cell) -> Tuple[float, float]:
        return (
            self._origin.x + (float(cell._ix) + 0.5)*(self._extent.x - self._origin.x)/self._nx,
            self._origin.y + (float(cell._iy) + 0.5)*(self._extent.y - self._origin.y)/self._ny
        )

    def get_cell_from_coordinates(self, x: float, y: float) -> Cell:
        eps = 1e-6*max(
            (self._extent.x-self._origin.x)/self._nx,
            (self._extent.y-self._origin.y)/self._ny
        )
        if abs(x - self._extent.x) < eps:
            ix = self._nx - 1
        elif abs(x - self._origin.x) < eps:
            ix = 0
        else:
            ix = int((x - self._origin.x)/((self._extent.x - self._origin.x)/self._nx))
        if abs(y - self._extent.y) < eps:
            iy = self._ny - 1
        elif abs(y - self._origin.y) < eps:
            iy = 0
        else:
            iy = int((y - self._origin.y)/((self._extent.y - self._origin.y)/self._ny))
        return self.Cell(ix, iy)


def test_number_of_cells():
    assert RasterGrid(Point(0.0,0.0), [1.0,1.0], 10, 10).nc == 100
    assert RasterGrid(Point(0.0,0.0), [1.0,1.0], 10, 20).nc == 200
    assert RasterGrid(Point(0.0,0.0), [1.0,1.0], 20, 10).nc == 200
    assert RasterGrid(Point(0.0,0.0), [1.0,1.0], 20, 20).nc == 400


def test_locate_cell():
    grid = RasterGrid(Point(0.0,0.0), [2.0,2.0], 2, 2)
    cell = grid.get_cell_from_coordinates(0, 0)
    assert cell._ix == 0 and cell._iy == 0
    cell = grid.get_cell_from_coordinates(1, 1)
    assert cell._ix == 1 and cell._iy == 1
    cell = grid.get_cell_from_coordinates(0.5, 0.5)
    assert cell._ix == 0 and cell._iy == 0
    cell = grid.get_cell_from_coordinates(1.5, 0.5)
    assert cell._ix == 1 and cell._iy == 0
    cell = grid.get_cell_from_coordinates(0.5, 1.5)
    assert cell._ix == 0 and cell._iy == 1
    cell = grid.get_cell_from_coordinates(1.5, 1.5)
    assert cell._ix == 1 and cell._iy == 1


def test_cell_center():
    grid = RasterGrid(Point(0.0,0.0), [2.0,2.0], 2, 2)
    cell = grid.get_cell_from_coordinates(0.5, 0.5)
    assert abs(grid.get_center_coordinates(cell)[0] - 0.5) < 1e-7 and abs(grid.get_center_coordinates(cell)[1] - 0.5) < 1e-7
    cell = grid.get_cell_from_coordinates(1.5, 0.5)
    assert abs(grid.get_center_coordinates(cell)[0] - 1.5) < 1e-7 and abs(grid.get_center_coordinates(cell)[1] - 0.5) < 1e-7
    cell = grid.get_cell_from_coordinates(0.5, 1.5)
    assert abs(grid.get_center_coordinates(cell)[0] - 0.5) < 1e-7 and abs(grid.get_center_coordinates(cell)[1] - 1.5) < 1e-7
    cell = grid.get_cell_from_coordinates(1.5, 1.5)
    assert abs(grid.get_center_coordinates(cell)[0] - 1.5) < 1e-7 and abs(grid.get_center_coordinates(cell)[1] - 1.5) < 1e-7


def test_cell_iterator() -> None:
    grid = RasterGrid(Point(0.0,0.0), [2.0,2.0], 2, 2)
    count = sum(1 for _ in grid.cells)
    assert count == grid.nc

    cell_indices_without_duplicates = set(list(
        (cell._ix, cell._iy) for cell in grid.cells
    ))
    assert len(cell_indices_without_duplicates) == count

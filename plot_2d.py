from typing import List, Iterable
from dataclasses import dataclass
from matplotlib.pyplot import figure, show


@dataclass
class Point:
    x: float
    y: float


class SquareLattice:
    def __init__(self,
                 lower_left: Point,
                 size: List[float],
                 resolution: List[int]) -> None:
        self._lower_left = lower_left
        self._size = size
        self._resolution = resolution

    def points(self) -> Iterable[Point]:
        dx = (
            self._size[0]/self._resolution[0],
            self._size[1]/self._resolution[1]
        )
        return (
            Point(
                self._lower_left.x + (float(i) + 0.5)*dx[0],
                self._lower_left.y + (float(j) + 0.5)*dx[1]
            )
            for j in range(self._resolution[1])
            for i in range(self._resolution[0])
        )


def evaluate_field(point: Point) -> float:
    x, y = point.x, point.y
    return 1.0/((1.0 - x)*(5.0 - x)) + 1.0/((1.0 - y)*(5.0 - y))


def initialize(p0: Point,
               size: List[float],
               resolution: List[int]) -> None:
    p0.x = 1.0
    p0.y = 1.0
    size[0] = 4.0
    size[1] = 4.0
    resolution[0] = 25
    resolution[1] = 25


def plot(lattice: SquareLattice) -> None:
    x, y, z = [], [], []
    for p in lattice.points():
        x.append(p.x)
        y.append(p.y)
        z.append(evaluate_field(p))

    fig = figure()
    ax = fig.add_subplot(projection='3d')
    img = ax.scatter(x, y, z)
    fig.colorbar(img)
    show()


if __name__ == "__main__":
    p0 = Point(0.0, 0.0)
    size = [0.0, 0.0]
    resolution = [0, 0]
    initialize(p0, size, resolution)
    lattice = SquareLattice(p0, size, resolution)
    plot(lattice)

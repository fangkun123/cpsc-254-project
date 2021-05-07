"""
Game data manager
Use None for unfilled, False for black, and True for white.
The manager provides related access interfaces.
"""

from collections import defaultdict
from typing import Tuple, Union, NoReturn, Iterator, Set, Dict, Optional


class Manager:
    """
    Game data manager
    Use a two-dimensional array matrix to represent the game board.
    """

    def __init__(self, size: int) -> NoReturn:
        """
        Initialize a new game data manager.
        Parameters:
            size: int - length and width of the game board (same)
        """
        self._size = size
        self._board = [
            [None for _index in range(size)]
            for _index in range(size)
        ]

    @property
    def size(self) -> int:
        """Return size of game board"""
        return self._size

    def _around(self, _x: int, _y: int) -> Iterator[Tuple[int, int]]:
        """Return all grids's indexs around specific grid"""
        if _x >= self._size or _y >= self._size:
            raise IndexError("Invalid index for ({x}, {y})".format(x=_x, y=_y))

        for i in (_x - 1, _x, _x + 1):
            for j in (_y - 1, _y, _y + 1):
                if (i, j) == (_x, _y):
                    continue
                if i < 0 or j < 0:
                    continue
                if i >= self._size or j >= self._size:
                    continue
                yield (i, j)

    def find(self, row: int, column: int, paths: Dict[int, Set[Tuple[int]]],
             direction: Optional[int] = None) -> NoReturn:
        """
        Try to continuously find the specified amount
        of continuously set data in any direction
        Parameters:
            row, column: position or grid
            paths: path for all directions
            directions:
            1   2   3
              ↖ ↑ ↗
            4 ← · → 4
              ↙ ↓ ↘
            3   2   1
        """
        target = self[row, column]

        # Check if already some direction has already find enough
        for index in range(1, 5):
            if len(paths[index]) == 5:
                return

        # Find all grids aorund current one
        around = self._around(row, column)
        classified = defaultdict(list)
        for nrow, ncolumn in around:

            # Filter all invalid grid
            if not self[nrow, ncolumn] == target:
                continue

            # Define direction
            if (nrow - row) * (ncolumn - column) == 1:
                classified[1].append((nrow, ncolumn))
            if nrow - row == 0:
                classified[2].append((nrow, ncolumn))
            if (nrow - row) * (ncolumn - column) == -1:
                classified[3].append((nrow, ncolumn))
            if ncolumn - column == 0:
                classified[4].append((nrow, ncolumn))

        # If direction has not been specified
        if direction is None:
            for ndirection, grids in classified.items():
                for nrow, ncolumn in grids:
                    paths[ndirection].add((row, column))
                    paths[ndirection].add((nrow, ncolumn))
                    self.find(nrow, ncolumn, paths, ndirection)

        # If direction has been sprcified
        else:
            grids = classified[direction]
            for nrow, ncolumn in grids:
                if (nrow, ncolumn) in paths[direction]:
                    continue
                paths[direction].add((nrow, ncolumn))
                self.find(nrow, ncolumn, paths, direction)

    def __setitem__(self, index: Tuple[int, int], value: Union[None, bool]) -> NoReturn:
        """Set status for specific index of grid"""
        _x, _y = index
        if _x > self._size or _x < 0 or _y > self._size or _y < 0:
            raise IndexError("Invalid index for ({x}, {y})".format(x=_x, y=_y))

        # Check for grid if grid has been set
        if isinstance(self._board[_x][_y], bool) and not value is None:
            raise ValueError("Cannot set grid which has already been set")
        self._board[_x][_y] = value

    def __getitem__(self, index: Tuple[int, int]) -> Union[None, bool]:
        """Return status for specific index of grid"""
        _x, _y = index
        if _x > self._size or _x < 0 or _y > self._size or _y < 0:
            raise IndexError("Invalid index for ({x}, {y})".format(x=_x, y=_y))
        return self._board[_x][_y]

    def show(self) -> NoReturn:
        """Show all grids status"""
        status = list()
        for row in self._board:
            for column in row:
                if column is None:
                    status.append('x ')
                if column is True:
                    status.append('N ')
                if column is False:
                    status.append('Y ')
            status.append('\n')
        print(''.join(status))

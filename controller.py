"""
Controller
Collect game initialization data
Instantiate data classes and interface
classes and make them work together.
"""

import tkinter
from collections import defaultdict
from typing import NoReturn, Union

from view import Board
from model import Manager


class Gomoku:
    """
    Gomoku Game
    Instantiate model class and view class
    Bind the appropriate processing function to the interface
    Send the interface data to the data class for processing
    """
    TITLE = "Gomoku"  # Game window title

    def __init__(self, size: int, grids: int) -> NoReturn:
        """
        Initialiaze a new Gomoku game
        Parameters:
            size: game board size
            grids: total grids in each direction
        """
        self._size, self._grids = size, grids

        # New Tk instance
        self._window = tkinter.Tk()
        self._window.title(self.TITLE)
        self._window.resizable(False, False)

        # Game paras
        self._turn = None
        self._model = Manager(grids - 1)
        self._view = Board(self._window, size, grids)
        self._view.bind_left_key(self._handler)
        self._view.bind_moving(self._hint)
        self._view.bind_restart(self.restart)

    @property
    def turn(self) -> Union[None, bool]:
        """
        Return current game turn info
        Return:
            None - when game not start or already end
            False - black player's turn
            True - white player's turn
        """
        return self._turn

    def restart(self) -> NoReturn:
        """Restart a new game"""
        self._window.destroy()
        self.__init__(self._size, self._grids)
        self.start()

    def _handler(self, row: int, column: int) -> NoReturn:
        """Handle click event"""
        # Check if alreday end or not start
        if self._turn is None:
            return

        try:
            self._model[row, column] = self._turn
        except ValueError as _error:
            return
        color = "black" if not self._turn else "white"
        self._turn = not self._turn
        self._view.play(row, column, color)

        # Change hinter color
        target = self._view.hinter
        hintcolor = self._view.BHINT if not self._turn else self._view.WHINT
        self._view.canvas.itemconfig(target, fill=hintcolor)

        # Check if some player alreday win
        paths = defaultdict(set)
        self._model.find(row, column, paths)
        for _direction, grids in paths.items():
            if len(grids) == 5:
                who = "Black" if self._turn else "White"
                self._view.win(who)
                self._turn = None

    def _hint(self, _x: int, _y: int) -> NoReturn:
        """Show hint pieces"""
        # pylint: disable=invalid-name
        target = self._view.hinter
        xa, ya, xb, yb = self._view.canvas.coords(target)
        nx, ny = (xa + xb) / 2, (ya + yb) / 2
        dx, dy = _x - nx, _y - ny
        self._view.canvas.move(target, dx, dy)

    def start(self) -> NoReturn:
        """Draw game window and start"""
        self._turn = False
        self._view.draw()
        self._window.focus_get()
        self._window.mainloop()

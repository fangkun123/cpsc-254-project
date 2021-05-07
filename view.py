"""
Draw game interface
Use Tkinter and Canvas to draw interface
Provide a way to draw pieces
"""

import tkinter
import tkinter.messagebox as msg
from typing import NoReturn, Callable


class Board:
    """
    Gaming Board Interface
    Use canvas to draw horizontal and vertical lines
    Handle mouse click events, generate click
    position parameters and pass them to the middle layer
    """
    # White space between the edge of the
    # window and the main interface of the game
    PADDING = 20
    ICONMAP = "logo.ico"

    BGCOLOR = "#FEBE0B"  # Background color for game board
    BHINT = "#333333"  # Black hinter
    WHINT = "#F0F0F0"  # White hinter

    def __init__(self, root: tkinter.Tk, size: int, grids: int) -> NoReturn:
        """
        Instantiate a new game board object.
        Draw on the given parent Tk object.
        Parameters:
            root: in which window you want to draw
            size: total game window size
            grids: number of grids (usually 15 or 19)
        """
        # Patch for invalid size and grids
        self._root = root
        self._grids, self._size = grids, size
        if self._size % grids != 0:
            self._size = (self._size // grids) * grids

        # Draw canvas
        self._root = root
        self._board = tkinter.Canvas(
            root, width=self._size + self.PADDING * 2,
            height=self._size + self.PADDING * 2, bg=self.BGCOLOR)
        self._board.pack(anchor=tkinter.CENTER)
        self._unit = self._size // grids
        self._board.focus_set()

        # Draw hint piece
        piece = int(self._unit / 3.0)
        self._hinter = self._board.create_oval(
            0, 0, -piece * 2, -piece * 2,
            fill=self.BHINT, outline="")

        # Bind left key and moving
        self._board.bind("<Button-1>", self._left_key)
        self._board.bind("<Motion>", self._moving)

        # Handle left key function
        self._left_key_handler = None
        self._moving_handler = None
        self._restart_function = None

        # Initial menubar
        menubar = tkinter.Menu(self._root)
        about = tkinter.Menu(menubar)
        controller = tkinter.Menu(menubar)
        menubar.add_cascade(label="Game", menu=controller)
        menubar.add_cascade(label="About", menu=about)

        controller.add_command(label="New Game", command=self.restart)
        controller.add_separator()
        controller.add_command(label="Exit Game", command=self._exit)

        about.add_command(label="Help", command=self._help)
        about.add_command(label="About", command=self._about)
        root.configure(menu=menubar)

        # Configure icon
        root.iconbitmap(self.ICONMAP)

    def bind_restart(self, handler) -> NoReturn:
        """Bind restart function"""
        self._restart_function = handler

    def restart(self) -> NoReturn:
        """Retstart a new game - abstract"""
        if not self._restart_function is None:
            self._restart_function()

    def _exit(self) -> NoReturn:
        """Destory window and exit game"""
        self._root.destroy()
        __import__("sys").exit(0)

    def _help(self) -> NoReturn:
        """Show help dialog"""
        msg.showinfo("Help", (
            "Please choose the appropriate location.\n"
            "The color of the chess piece following the "
            "prompt of the mouse is the color of the "
            "upcoming chess piece."
        ))

    def _about(self) -> NoReturn:
        """Show about info"""
        msg.showinfo("About", (
            "This is a simple Gomoku game.\n"
            "Wish you a happy game!"
        ))

    @property
    def size(self) -> int:
        """Return game board size"""
        return self._size

    @property
    def canvas(self) -> tkinter.Canvas:
        """Return canvas"""
        return self._board

    @property
    def hinter(self) -> int:
        """Return hinter"""
        return self._hinter

    def bind_left_key(self, function: Callable[[int, int], NoReturn]) -> NoReturn:
        """Bind function to click handler"""
        self._left_key_handler = function

    def bind_moving(self, function: Callable[[int, int], NoReturn]) -> NoReturn:
        """Bind function to moving and drag"""
        self._moving_handler = function

    def _left_key(self, position: tkinter.Event) -> NoReturn:
        """Handle for left key click event"""
        _x, _y = position.x - self.PADDING, position.y - self.PADDING
        _x -= self._unit // 2
        _y -= self._unit // 2
        if _x < 0 or _y < 0:
            return
        row, column = _x // self._unit, _y // self._unit
        if row >= self._grids - 1 or column >= self._grids - 1:
            return

        # Reduce row and column data to handler
        if not self._left_key_handler is None:
            self._left_key_handler(row, column)

    def _moving(self, position: tkinter.Event) -> NoReturn:
        """Handle moving event"""
        # Reduce moving event
        if not self._moving_handler is None:
            self._moving_handler(position.x, position.y)

    def play(self, row: int, column: int, color: str) -> NoReturn:
        """Drop off at the specified position"""
        _x = (row + 1) * self._unit + self.PADDING
        _y = (column + 1) * self._unit + self.PADDING
        radius = int(self._unit / 3.0)
        position = _x - radius, _y - radius, _x + radius, _y + radius
        self._board.create_oval(*position, fill=color, outline="")

    def win(self, who: str) -> NoReturn:
        """Show congratulations"""
        msg.showinfo("Congratulations", "{player} win!".format(player=who))

    def draw(self) -> NoReturn:
        """Draw vertical and horizontal lines as the game board"""
        for index in range(self._grids + 1):
            # Draw horizontal
            startx = self.PADDING, self.PADDING + self._unit * index
            endx = self.PADDING + self._size, self.PADDING + self._unit * index
            self._board.create_line(*startx, *endx)

            # Draw vertical
            starty = self.PADDING + index * self._unit, self.PADDING
            endy = self.PADDING + index * self._unit, self.PADDING + self._size
            self._board.create_line(*starty, *endy)

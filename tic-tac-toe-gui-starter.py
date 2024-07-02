import tkinter as tk


class Cell:
    """
    Attributes
    - state: "O" or "X" i.e., mark of the cell
    - pos: [i,j] i.e., the row and column position of the cell

    Methods
    - check(mark): marks the cell as "O" or "X" based on mark
    - clear(): resets the cell state to ""
    """
    def __init__(self, pos=[0, 0]):
        """
        attributes
        state: "O" or "X"
        """
        self.state = ""
        self.pos = pos

    def check(self, mark="O"):
        self.state = mark

    def clear(self):
        self.state = ""


class Player:
    """
    Attributes
    - mark: current player-mark i.e. "O" or "X"

    Methods
    - switch: switches player-mark; called after processing a game step
    """
    def __init__(self, mark='O'):
        self.mark = mark

    def switch(self):
        """
        if self.mark == 'O': self.mark = ...
        else: ....
        """
        return


class Board:
    """
    Attributes
    - player: A Player object; used to identify player's turn
    - cells: A 2D list of Cell objects (size: 3x3); note: cells[0][1].state gives the state of the cell in the 1st row 2nd column.

    Methods
    - is_full(): if no cell state is empty; run a nested loop for all the cells and count if cells[i][j].state == ""
    - is_win(recent_mark_pos): for recent_mark_pos=[i,j],
                            returns True:
                                if the states of the i-th row are all the same (player.mark) or
                                if the states of the j-th col are all the same (player.mark) or
                                if the states of the either diagonal are all equal to the player.mark
    - update(recent_mark_pos): Runs a game step for after checking a mark.
                            returns "win" : if is_win()
                            returns "draw": if is_full()
                            otherwise, switches the player mark using player.switch()
    """
    def __init__(self, cell_class=Cell, player_class=Player, *args):
        self.player = player_class()
        self.cells = []
        for i in range(3):
            row = []
            for j in range(3):
                row.append(cell_class([i,j], *args))
            self.cells.append(row)

    def is_full(self):
        empty_cnt = 0
        for i in range(3):
            for j in range(3):
                if self.cells[i][j].state == "": empty_cnt += 1
        if empty_cnt == 0: return True
        else: return False

    def is_win(self, recent_mark_pos):
        i, j = recent_mark_pos
        mark = self.player.mark

        # check i-th row
        if all(self.cells[i][col].state == mark for col in range(3)):
            return True
        # check j-th col
        if all(self.cells[row][j].state == mark for row in range(3)):
            return True
        # check left diagonal
        if i == j and all(self.cells[d][d].state == mark for d in range(3)):
            return True
        # check right diagonal
        if i + j == 2 and all(self.cells[d][2 - d].state == mark for d in range(3)):
            return True

        return False

    def update(self, recent_mark_pos):
        pass


class CellGUI(Cell):
    """
    Extends the Cell class
    Additional Attributes
    - board: A Board object
    - button: A tkinter Button object that handles click from the user

    Additional methods
    - on_click(): checks the cell, changes the button text, calls for board update
    """
    def __init__(self, pos=[0, 0], board=None):
        super().__init__(pos)
        self.board = board
        self.button = tk.Button(master=self.board.board_frame, text=self.state, height=2, width=5, command=self.on_click)

    def on_click(self):
        self.check(self.board.player.mark)
        self.button.configure(text=self.state)
        self.board.update(self.pos)


class BoardGUI(Board):
    """
    Extends the Board class.
    Additional attributes
    - board_frame: A tkinter Frame object that holds the CellGUI objects
    - msg_label: A tkinter Label object that shows the current game status

    Additional methods
    - update(recent_mark_pos):
            Calls the update method of superclass;
            Based on the return value of that call, it updates the msg_label status
    """
    def __init__(self, cell_class=CellGUI, player_class=Player):
        root = tk.Tk()
        root.title("TicTacToe")
        root.maxsize(900, 600)
        root.config(bg="skyblue")

        self.board_frame = tk.Frame(master=root)
        super().__init__(cell_class, player_class, self)
        for i in range(3):
            for j in range(3):
                self.cells[i][j].button.grid(row=i, column=j)
        self.board_frame.pack()

        self.msg_label = tk.Label(master=root, text="Player {}'s turn".format(self.player.mark))
        self.msg_label.pack()

        self.root = root
        self.root.mainloop()

    def update(self, recent_mark_pos):
        res = super().update(recent_mark_pos)
        if res == "win":
            self.msg_label.configure(text="Player-{} Won!".format(self.player.mark))
            return
        elif res == "draw":
            self.msg_label.configure(text="Match Draw!")
            return
        self.msg_label.configure(text="Player {}'s turn".format(self.player.mark))


board = BoardGUI()







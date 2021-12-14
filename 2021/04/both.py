"""
Finds the first and the last winning bingo boards.
"""
import pprint


class BoardSquare:
    def __init__(self, t_num):
        """
        Represents a square of the board.

        The square can be marked (<picked> = True)
        and always contains a number (<number>)
        """
        self.number = t_num
        self.picked = False
    
    def __repr__(self) -> str:
        return str(self.number)


class Board:
    def __init__(self, t_grid):
        """
        Represents a board.

        A board is a grid of BoardSquare squares.
        """
        self.row_len = len(t_grid)
        try:
            self.col_len = len(t_grid[0])
        except IndexError:
            raise ValueError("<t_grid> should be a matrix")
        
        if self.row_len != self.col_len:
            raise ValueError("<t_grid> should have the same number of columns and rows")
        
        self.grid = t_grid
        self.last_pick = None
        self.winning_pick = None

    def is_winner(self):
        """
        Returns true if this board is a winning board.

        A board is a winning board if a row or a column
        contains picked/marked numbers.
        """
        winner = False

        # find a winner row
        for row in self.grid:
            winner_row = True
            for el in row:
                if not el.picked:
                    winner_row = False
                    break
            
            if winner_row:
                winner = True
                break
        
        # find a winner column
        # > if a winner row wasn't found before
        if not winner:
            for c in range(self.col_len):
                winner_col = True
                for r in range(self.row_len):
                    if not self.grid[r][c].picked:
                        winner_col = False
                        break
                
                if winner_col:
                    winner = True
                    break
        
        if winner:
            self.winning_pick = self.last_pick

        return winner
    
    def set_picked(self, t_num):
        """
        If <t_num> is present in the board,
        set the board square to "picked"/marked.
        """
        found = False
        for row in self.grid:
            for el in row:
                if el.number == t_num:
                    el.picked = True
                    self.last_pick = t_num
                    found = True
                    break
            
            if found:
                break
    
    def get_score(self):
        """
        Calculate the score of the winning board
        by calculating the sum of the "non winning" numbers
        and by multipling the result by the winning pick
        """
        if self.winning_pick is None:
            raise ValueError("<winning_pick> is None: use set_picked() to find at least one number in the board")

        not_picked_sum = 0
        for row in self.grid:
            for el in row:
                if not el.picked:
                    not_picked_sum += el.number
        
        return not_picked_sum * self.winning_pick


    def __repr__(self) -> str:
        return pprint.pformat(self.grid)


def parse_board(t_board_string):
    """
    Given a board string, this function converts
    it into a Board object.

    Example of board string:
     3 55 15 54 81
    56 77 20 99 25
    90 57 67  0 97
    28 45 69 84 14
    91 94 39 36 85
    """
    t_board_string = t_board_string.strip()

    board_grid = []
    for line in t_board_string.splitlines():
        no_dup_spaces = line.replace("  ", " ").strip()
        print("parsing '{}'...".format(no_dup_spaces))
        row_numbers = []

        for num in no_dup_spaces.split(" "):
            print("converting '{}' to a board square...".format(num))
            row_numbers.append(BoardSquare(int(num)))
        print("---")
        board_grid.append(row_numbers)

    return Board(board_grid)


if __name__ == "__main__":

    boards = []
    
    try:
        with open("input.txt", "r") as f:
            line = f.readline()
            rand_numbers = [int(num) for num in line.strip().split(",")]

            line = f.readline()
            board_string = line
            while line != "":
                board_string += line
                if line.strip() == "" and board_string.strip() != "":
                    board = parse_board(board_string)
                    boards.append(board)
                    board_string = ""

                line = f.readline()

    except FileNotFoundError:
        print("input.txt file doesn't exist")
        exit(1)
    except ValueError:
        print("couldn't parse the input data: found NaN")
        exit(2)
        
    print("=" * 20)
    print("\n# PARSED DATA:")
    print("random numbers picked:")
    print(rand_numbers)
    print("\nboards:")
    for board in boards:
        print(board)
        print("-" * 10)
    
    print("=" * 20)
    print("\n# SETTING PICKED NUMBERS AS PICKED\n")
    winner_board = None
    last_winner_board = None
    winners = 1
    for num in rand_numbers:
        for board in boards:
            print("checking:")
            print(board)
            print("checking if {} is present in the board".format(num))
            if not board.is_winner():
                board.set_picked(num)

                if board.is_winner():
                    if winners == 1:
                        print("found the first winner")
                        winner_board = board
                    elif winners == len(boards):
                        last_winner_board = board
                    winners += 1
            print("-"*10)
    
    print("=" * 20)
    print("\n# WINNERS:\n")
    print("first winner:")
    print(winner_board)
    print("board score:", winner_board.get_score())

    print("\nlast winner:")
    print(last_winner_board)
    print("board score:", last_winner_board.get_score())

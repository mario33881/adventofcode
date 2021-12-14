"""
Finds the lowest points of a 2D plane.
"""
import pprint

boold = False


def read_line_by_line(t_filepath):
    """
    Reads <t_filepath> file and yields one line at a time.
    """
    with open(t_filepath, "r") as f:
        line = f.readline()
        while line != "":
            yield line
            line = f.readline()


def find_minimums(t_list):
    """
    Find the values set between two greater values.

    Example:
    t_list = [1, 2, 5, 2, 7]
    points = [0, 3]

    Because 1 (in position 0) is less than 2
    and 2 (in position 3) is both less than 5 and 7
    """
    points = []
    length = len(t_list)
    i = 0
    while i < length:
        if i == 0:
            if t_list[i+1] > t_list[i]:
                # first point is smaller then the second point
                points.append(i)
        elif i == length - 1:
            if t_list[i] < t_list[i-1]:
                # last point is smaller than the previous one
                points.append(i)
        else:
            if t_list[i-1] > t_list[i] and t_list[i] < t_list[i+1]:
                # the current point is smaller than the two next to him
                points.append(i)
        
        i += 1

    return points


def transpose(t_matrix):
    """
    Calculate the transpose of a matrix.

    The transpose of a matrix contains the same values
    as the original matrix but the rows become the columns
    and viceversa.
    """
    tr_mat = []

    n_rows = len(t_matrix)
    n_cols = len(t_matrix[0])

    for c in range(n_cols):
        tr_row = []    
        for r in range(n_rows):
            tr_row.append(grid[r][c])
        
        tr_mat.append(tr_row)
    
    return tr_mat


def make_points(t_rows, t_cols):
    """
    Given two lists of x and y values,
    returns a list of points.

    These points are all the possible 
    combinations of those x and y values.
    """
    points = []
    for row in t_rows:
        for col in t_cols:
            for x in row:
                for y in col:
                    c = Coordinates(x, y)
                    points.append(c)
    
    return points


class Coordinates:
    def __init__(self, x, y):
        """
        Memorizes coordinates in a 2D plane.
        """
        self.x = x
        self.y = y
    
    def __str__(self):
        """User representation"""
        return "({}, {})".format(self.x, self.y)
    
    def __repr__(self):
        """Definition representation"""
        return "Coordinates" + self.__str__()
    
    def __eq__(self, __o: object) -> bool:
        return self.x == __o.x and self.y == __o.y
    
    def __hash__(self) -> int:
        return self.x * 1000 + self.y


def check_near_points(t_matrix, t_coordinates):
    """
    Checks if near poins are "valid points".

    A point is valid if the above, below, and sides values
    are greater than the current value.
    """
    valid_points = []

    for c in t_coordinates:

        if c.x in [0, len(t_matrix[0])-1] or c.y in [0, len(t_matrix)-1]:
            # point on the borders
            if c.x == 0 and c.y == 0:
                # top left
                if t_matrix[c.y][c.x] < t_matrix[c.y+1][c.x] \
                    and t_matrix[c.y][c.x] < t_matrix[c.y][c.x+1]:
                    valid_points.append(c)
            elif c.x == len(t_matrix[0])-1 and c.y == 0:
                # top right
                if t_matrix[c.y][c.x] < t_matrix[c.y+1][c.x] \
                    and t_matrix[c.y][c.x] < t_matrix[c.y][c.x-1]:
                    valid_points.append(c)

            elif c.x == 0 and c.y == len(t_matrix)-1:
                # bottom left
                if t_matrix[c.y][c.x] < t_matrix[c.y-1][c.x] \
                    and t_matrix[c.y][c.x] < t_matrix[c.y][c.x+1]:
                    valid_points.append(c)

            elif c.x == len(t_matrix[0])-1 and c.y == len(t_matrix)-1:
                # bottom right
                if t_matrix[c.y][c.x] < t_matrix[c.y-1][c.x] \
                    and t_matrix[c.y][c.x] < t_matrix[c.y][c.x-1]:
                    valid_points.append(c)
            else:
                # on borders, not on angles
                if c.x == 0:
                    # left border, not on angles
                    if t_matrix[c.y][c.x] < t_matrix[c.y-1][c.x] \
                        and t_matrix[c.y][c.x] < t_matrix[c.y+1][c.x] \
                        and t_matrix[c.y][c.x] < t_matrix[c.y][c.x+1]:
                        valid_points.append(c)
                
                elif c.x == len(t_matrix[0])-1:
                    # right border
                    if t_matrix[c.y][c.x] < t_matrix[c.y-1][c.x] \
                        and t_matrix[c.y][c.x] < t_matrix[c.y+1][c.x] \
                        and t_matrix[c.y][c.x] < t_matrix[c.y][c.x-1]:
                        valid_points.append(c)
                    
                elif c.y == 0:
                    # top border
                    if t_matrix[c.y][c.x] < t_matrix[c.y][c.x-1] \
                        and t_matrix[c.y][c.x] < t_matrix[c.y][c.x+1] \
                        and t_matrix[c.y][c.x] < t_matrix[c.y+1][c.x]:
                        valid_points.append(c)
                else:
                    # bottom border, not on angles
                    if t_matrix[c.y][c.x] < t_matrix[c.y][c.x-1] \
                        and t_matrix[c.y][c.x] < t_matrix[c.y][c.x+1] \
                        and t_matrix[c.y][c.x] < t_matrix[c.y-1][c.x]:
                        valid_points.append(c)

        else:
            # generic point
            if t_matrix[c.y][c.x] < t_matrix[c.y-1][c.x] \
                    and t_matrix[c.y][c.x] < t_matrix[c.y+1][c.x] \
                    and t_matrix[c.y][c.x] < t_matrix[c.y][c.x-1] \
                    and t_matrix[c.y][c.x] < t_matrix[c.y][c.x+1]:
                        valid_points.append(c)
    
    return valid_points


if __name__ == "__main__":

    # -- INPUT PARSING

    grid = []
    for line in read_line_by_line("input.txt"):
        v_line = [int(i) for i in line.strip()]
        grid.append(v_line)

    # -- FIND LOWEST POINTS
    #
    # To find the lowest points, It is possible to use derivatives of two variables.
    # Currently I only know I to do it if I have the formula f(x, y) = ...
    #
    
    rows_minimums = []
    for row in grid:
        rows_minimums.append(find_minimums(row))
    
    columns_minimums = []
    for tr_row in transpose(grid):
        columns_minimums.append(find_minimums(tr_row))

    if boold:
        pprint.pprint(rows_minimums)
        pprint.pprint(columns_minimums)

    points = make_points(rows_minimums, columns_minimums)
    if boold:
        pprint.pprint(points)

    valid = check_near_points(grid, points)
    if boold:
        pprint.pprint(valid)

    print("-"*10)
    unique_valid = set(valid)
    if boold:
        pprint.pprint(unique_valid)
    
    risk_levels_sum = 0
    for point in unique_valid:
        risk_level = 1 + grid[point.y][point.x]
        risk_levels_sum += risk_level
    
    print("risk levels sum", risk_levels_sum)

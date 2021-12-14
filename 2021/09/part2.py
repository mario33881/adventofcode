"""
Finds the 3 largest basins inside a cave.
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


class Coordinates:
    def __init__(self, x, y):
        """
        Memorizes coordinates in a 2D plane and the nearest points.

        Points are considered "near points" if they are above,
        below or on the sides of the point
        """
        self.x = x
        self.y = y
        self.near = []
    
    def __str__(self):
        """User representation"""
        return "({}, {})".format(self.x, self.y)
    
    def __repr__(self):
        """Definition representation"""
        return "Coordinates" + self.__str__()
    
    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, Coordinates):
            # don't attempt to compare against unrelated types
            return NotImplemented
        return (self.x == __o.x and self.y == __o.y)
    
    def __hash__(self) -> int:
        return self.x * 1000 + self.y


def get_near_coordinates(t_point, x_max, y_max):
    """
    Given a <t_point> point and the maximum possible coordinates (x_max, y_max),
    returns the nearest coordinates of the <t_point> point.

    Points are considered "near points" if they are above,
    below or on the sides of the point.
    """
    left = Coordinates(t_point.x-1, t_point.y)
    right = Coordinates(t_point.x+1, t_point.y)
    top = Coordinates(t_point.x, t_point.y-1)
    bottom = Coordinates(t_point.x, t_point.y+1)

    near = []

    if 0 <= left.x <= x_max and 0 <= left.y <= y_max:
        near.append(left)
    
    if 0 <= right.x <= x_max and 0 <= right.y <= y_max:
        near.append(right)
    
    if 0 <= top.x <= x_max and 0 <= top.y <= y_max:
        near.append(top)
    
    if 0 <= bottom.x <= x_max and 0 <= bottom.y <= y_max:
        near.append(bottom)
    
    return near
    

def set_basin(t_basin, t_point, t_points):
    """
    Recursively find all the nearest points that belongs to the <t_basin> basin.

    <t_point> is one of the points inside the basin.
    > used recursively to find its nearest points
    
    <t_points> contains all the points that are inside all the basins.
    > this is used to get the nearest points of the nearest points
    """
    if boold:
        print("t_basin attuale: ", t_basin)
        print("t_point: ", t_point)
        print("t_point.near: ", t_point.near)

    if t_point in t_basin:
        if boold:
            print("point is already present in basin")
        return

    t_basin.append(t_point)

    for near_point in t_point.near:
        # get the near point that has their data about their nearest points
        real_near_point = None
        for real_near_point in t_points:
            if real_near_point == near_point:
                break
        
        # find points near the nearest points
        # > all these points belong to the basin 
        set_basin(t_basin, real_near_point, t_points)


if __name__ == "__main__":

    # -- INPUT PARSING

    grid = []
    for line in read_line_by_line("input.txt"):
        v_line = [int(i) for i in line.strip()]
        grid.append(v_line)

    # -- FIND 3 LARGEST BASINS

    # create a grid of the highest points (height = 9)
    highest_points_grid = []
    for row in grid:
        highest_points_row = []
        for el in row:
            if el == 9:
                highest_points_row.append(1)
            else:
                highest_points_row.append(0)
        
        highest_points_grid.append(highest_points_row)
    
    if boold:
        pprint.pprint(highest_points_grid)
    
    # find every but the highest points (and memorize their nearest points)
    points = []
    for r in range(len(highest_points_grid)):
        for c in range(len(highest_points_grid[r])):
            if highest_points_grid[r][c] == 0:
                p = Coordinates(c, r)

                # get all the nearest points to the point p
                near_points = get_near_coordinates(p, len(highest_points_grid[r])-1, len(highest_points_grid)-1)
                for point in near_points:
                    if highest_points_grid[point.y][point.x] == 0:
                        p.near.append(point)
                points.append(p)

    if boold:
        print("points and their near points that are 0:")
        for point in points:
            print(point.__dict__)
        print("there are {} points".format(len(points)))
        print("=" * 10)
    
    # find all the basins
    basins = {}
    basin_id = 0
    for point in points:
        point_in_basin = False
        for basin in basins.values():
            if point in basin:
                point_in_basin = True
                break
        
        if not point_in_basin:
            basin = []
            set_basin(basin, point, points)
            if boold:
                print("adding basin:", basin)
                print("")
            basins[basin_id] = basin
            basin_id += 1
        else:
            if boold:
                print("skipping because already present in a basin:", point)
    
    if boold:
        print("basins:")
        for basin in basins.values():
            pprint.pprint(basin)
            print("")
    
        print("="*10)

    # find the largest 3 basins

    biggest_3_basins = [0, 0, 0]
    biggest_3_basins_len = [0, 0, 0]
    for basin_data in basins.items():
        basin_id = basin_data[0]
        basin = basin_data[1]

        if boold:
            print("basin num {} is large {}".format(basin_id, len(basin)))
        if len(basin) > biggest_3_basins_len[0]:
            if boold:
                print("found larger basin")
            biggest_3_basins_len[0] = len(basin)
            biggest_3_basins[0] = basin_id

    if boold:
        print("")

    for basin_data in basins.items():
        basin = basin_data[1]
        basin_id = basin_data[0]
        if boold:
            print("basin num {} is large {}".format(basin_id, len(basin)))
        if len(basin) > biggest_3_basins_len[1] and basin_id != biggest_3_basins[0]:
            if boold:
                print("found larger basin")
            biggest_3_basins_len[1] = len(basin)
            biggest_3_basins[1] = basin_id
    
    if boold:
        print("")

    for basin_data in basins.items():
        basin = basin_data[1]
        basin_id = basin_data[0]
        if boold:
            print("basin num {} is large {}".format(basin_id, len(basin)))
        if len(basin) > biggest_3_basins_len[2] \
            and basin_id != biggest_3_basins[0] \
            and basin_id != biggest_3_basins[1]:
            if boold:
                print("found larger basin")
            biggest_3_basins_len[2] = len(basin)
            biggest_3_basins[2] = basin_id
    
    # -- OUTPUT

    print("")
    print("biggest 3 basins len:", [i for i in zip(biggest_3_basins, biggest_3_basins_len)])
    print("multiplication of 3 largest basins:", biggest_3_basins_len[0] * biggest_3_basins_len[1] * biggest_3_basins_len[2])

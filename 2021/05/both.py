"""
Maps hydrothermal vents on the ocean floor.
"""
import os

filepath = "input.txt"
part2 = True  # False -> part1, True -> part2
boold = False


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


def read_line_by_line(t_filepath):
    """
    Reads <t_filepath> file and yields one line at a time.
    """
    with open(t_filepath, "r") as f:
        line = f.readline()
        while line != "":
            yield line
            line = f.readline()


if __name__ == "__main__":

    if not os.path.isfile(filepath):
        print(filepath, "file doesn't exist")
        exit(1)

    lines_ends = []
    max_x = 0
    max_y = 0

    for line in read_line_by_line(filepath):
        strip_line = line.strip()
        v_strip_line = strip_line.split("->")

        if len(v_strip_line) == 2:
            line_end1, line_end2 = strip_line.split("->")
            line_end1 = line_end1.strip()
            line_end2 = line_end2.strip()

            line_end1_xy = line_end1.split(",")
            line_end2_xy = line_end2.split(",")
            coordinate_end1 = Coordinates(int(line_end1_xy[0]), int(line_end1_xy[1]))
            coordinate_end2 = Coordinates(int(line_end2_xy[0]), int(line_end2_xy[1]))
            lines_ends.append([coordinate_end1, coordinate_end2])
            if boold:
                print(coordinate_end1, coordinate_end2)

            if coordinate_end1.x > max_x:
                max_x = coordinate_end1.x
            
            if coordinate_end2.x > max_x:
                max_x = coordinate_end2.x
            
            if coordinate_end1.y > max_y:
                max_y = coordinate_end1.y
            
            if coordinate_end2.y > max_y:
                max_y = coordinate_end2.y
        else:
            print("incorrect input (lacks of '->'):", strip_line)

    diagram = []
    for r in range(max_x + 1):
        row = []
        for c in range(max_y + 1):
            row.append(0)
        
        diagram.append(row)

    if boold:
        print("Diagram dimensions:", len(diagram), len(diagram[0]))
    #pprint.pprint(diagram)

    for line in lines_ends:
        p1 = line[0]
        p2 = line[1]

        if boold:
            print(p1, p2, abs(p1.x - p2.x), abs(p2.y - p2.y))

        if p1.x == p2.x:
            # vertical line in (p1.x, y):
            # where y: p1.y --> p2.y or p1.y <-- p2.y
            starting_y = min(p1.y, p2.y)
            y_distance = abs(p1.y - p2.y)

            if boold:    
                print("found vertical line:", line)

            for y in range(starting_y, starting_y + y_distance + 1):
                if boold:
                    print("setting y = {} (from {} to {})".format(y, starting_y, starting_y + y_distance))
                diagram[y][p1.x] += 1

        elif p1.y == p2.y:
            # horizontal line in (x, p2.y)
            # where x: p1.x --> p2.x or p1.x <-- p2.x
            starting_x = min(p1.x, p2.x)
            x_distance = abs(p1.x - p2.x)
            
            if boold:
                print("found horizontal line:", line)

            for x in range(starting_x, starting_x + x_distance + 1):
                if boold:
                    print("setting x = {} (from {} to {})".format(x, starting_x, starting_x + x_distance))
                diagram[p1.y][x] += 1
        
        elif (abs(p1.x - p2.x) == abs(p1.y - p2.y)) and part2:
            # diagonal line at 45 degrees
            starting_y = min(p1.y, p2.y)
            if starting_y == p1.y:
                starting_x = p1.x
            else:
                starting_x = p2.x
            
            ending_y = max(p1.y, p2.y)
            if ending_y == p1.y:
                ending_x = p1.x
            else:
                ending_x = p2.x

            xy_distance = abs(p1.y - p2.y)  # distance is equal between start x - end x and start y - end y

            if boold:
                print("found diagonal line:", line)
                print("starting position: ", starting_x, starting_y)
                print("distance: ", xy_distance)

            if starting_x > ending_x:
                # line is: /
                for y in range(starting_y, ending_y + 1):
                    #print("y:", y)
                    for x in range(starting_x, ending_x - 1, -1):
                        #print("x:", x)
                        if abs(y - starting_y) == abs(x - starting_x):
                            if boold:
                                print("setting x = {}, y = {} (from {} to {})".format(starting_x, starting_y, p1, p2))
                            diagram[y][x] += 1
            else:
                # line is: \
                for y in range(starting_y, ending_y + 1):
                    #print("y:", y)
                    for x in range(starting_x, ending_x + 1):
                        #print("x:", x)
                        if abs(y - starting_y) == abs(x - starting_x):
                            if boold:
                                print("setting x = {}, y = {} (from {} to {})".format(starting_x, starting_y, p1, p2))
                            diagram[y][x] += 1

    dangerous_areas = 0
    for row in diagram:
        for el in row:
            if el >= 2:
                dangerous_areas += 1
    
    if part2:
        print("part 2 solution:")
    else:
        print("part 1 solution:")
    print("There are {} dangerous_areas".format(dangerous_areas))

"""
This script uses coordinates inside the input.txt file to find 
the position of the submarine.
"""
import os

file = "input.txt"


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


class Submarine:
    def __init__(self):
        """
        Represents a submarine.

        A submarine has:
        * position/coordinates: x is the horizontal position and y is the depth
        * actions: move forward, up and down
        """
        self.position = Coordinates(0, 0)
    
    def forward(self, value):
        """
        increases the horizontal position by <value> units
        """
        self.position.x += value
    
    def up(self, value):
        """
        decreases the depth by <value> units
        """
        self.position.y -= value
    
    def down(self, value):
        """
        increases the depth by <value> units
        """
        self.position.y += value


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

    submarine = Submarine()

    if not os.path.isfile(file):
        print("file '{}' doesn't exist".format(file))
        exit(1)

    for line in read_line_by_line(file):
        strip_line = line.strip()
        v_line = strip_line.split(" ")

        if len(v_line) == 2:
            try:
                action = v_line[0]
                value = int(v_line[1])

                if action == "forward":
                    submarine.forward(value)
                elif action == "down":
                    submarine.down(value)
                elif action == "up":
                    submarine.up(value)

            except ValueError:
                print("Couldn't convert {} value to integer".format(v_line[1]))
        else:
            print("Incorrect number of values in input, skipping:", v_line)

    final_position = submarine.position
    print("Final position:", final_position)
    print("puzzle answer:", final_position.x * final_position.y)

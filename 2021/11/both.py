"""
Counts how many time octopi flash in a 10x10 grid
and after how many steps they synchronize
"""
import pprint

boold = False
test_data_str = """5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526"""

test_data = test_data_str.splitlines()


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
        """Two coordinates are equal if they have the same x and y coordinates"""
        return self.x == __o.x and self.y == __o.y


class OctopiGrid:
    def __init__(self, grid) -> None:
        """
        Represents an octopi grid.

        Populates a matrix of Octopus objects
        and then sets inside each Octopus the
        fact that they are inside the same 10x10 grid.
        """
        self.grid = []
        self.n_flashes = 0
        self.all_flashing = False

        # grid contains the energy of each octopus.
        # use that grid to create an Octopus object with these attributes:
        # * coordinates: position of the octopus
        # * octopus energy: energy that the octopus can use to flash
        for r, row in enumerate(grid):
            octopy_row = []
            for c, octopus_energy in enumerate(row):
                octopus = Octopus(Coordinates(c, r), octopus_energy)
                octopy_row.append(octopus)
            
            self.grid.append(octopy_row)
        
        # now that the grid is populated, let each octopus know
        # where they all are
        for row in self.grid:
            for octopus in row:
                octopus.set_grid(self.grid)
    
    def step(self):
        """
        Calls octopus.step() to advance each octopus step,
        counts the total number of flashes across multiple steps and checks 
        if this step results in all the octopi to flash.

        After the step, all the flashing octopi go back to be
        "not flashing"
        """
        # each octopus "goes" one step forward
        for row in self.grid:
            for octopus in row:
                octopus.step()
        
        # check how many octopi are flashing and "turn them off"
        self.all_flashing = False
        current_flashes = 0
        for row in self.grid:
            for octopus in row:
                if octopus.isflashing:
                    self.n_flashes += 1
                    current_flashes += 1
                    octopus.isflashing = False
        
        # knowing that this is a 10x10 grid, when 100 octopi are flashing,
        # all of them are flashing
        if current_flashes == 100:
            self.all_flashing = True

    def __str__(self):
        return pprint.pformat(self.grid)
    
    def __repr__(self) -> str:
        return self.__str__()


class Octopus:

    def __init__(self, coordinates, initial_energy) -> None:
        """
        Represents an octopus.

        An Octopus is part of a grid of octopi (OctopiGrid object),
        has a position in that grid (Coordinates object),
        has energy that allows him to flash when its energy is greater than 9
        and flashes (isflashing = True)
        """
        self.grid = []
        self.position = coordinates
        self.energy = initial_energy
        self.isflashing = False
    
    def set_grid(self, grid):
        """
        Used by the OctopiGrid object to set the grid
        of this Octopus.
        """
        self.grid = grid

    def step(self):
        """
        During a step, an octopus:
        * increases its energy (unless it is already flashing)
        * flashes when it has enough energy (above 9)
        * when it flashes, its energy turns back to 0.
          Its flash results in its neighbors to "go up" one step as well.
        """
        if not self.isflashing:
            self.energy += 1

        if self.energy > 9:
            self.energy = 0
            self.isflashing = True
            self.increment_neighbors(self.position)
    
    def increment_neighbors(self, curr_pos):
        """
        The neighbors of this Octopus are next to it 
        vertically, horizontally or diagonally.
        """
        neighbors = [
            [Coordinates(curr_pos.x-1, curr_pos.y-1), Coordinates(curr_pos.x, curr_pos.y-1), Coordinates(curr_pos.x+1, curr_pos.y-1)],
            [Coordinates(curr_pos.x-1, curr_pos.y),   Coordinates(curr_pos.x, curr_pos.y),   Coordinates(curr_pos.x+1, curr_pos.y)],
            [Coordinates(curr_pos.x-1, curr_pos.y+1), Coordinates(curr_pos.x, curr_pos.y+1), Coordinates(curr_pos.x+1, curr_pos.y+1)]
        ]

        for row in neighbors:
            for neighbor_pos in row:
                if neighbor_pos != self.position:
                    # knowing that the grid is 10x10, a coordinate is valid if x and y are between 0 and 9 (included)
                    if neighbor_pos.x >= 0 and neighbor_pos.x <= 9 and neighbor_pos.y >= 0 and neighbor_pos.y <= 9:
                        neighbor = self.grid[neighbor_pos.y][neighbor_pos.x]
                        neighbor.step()

    def __str__(self) -> str:
        return str(self.energy)
    
    def __repr__(self) -> str:
        return self.__str__()


def part1(t_input):
    """
    The first part of the puzzle requests 
    the number of flashes after 100 steps.

    This function:
    1. parses the input to convert it into a grid of numbers
    2. creates a grid of Octopus objects using an OctopiGrid object
    3. calls octopy_grid.step() to make every Octopus in the OctopiGrid
       "go up" one step for 100 times and memorizes the total amount of flashes
    4. returns the total amount of flashes of every Octopus
    """
    n_grid = []
    for row in t_input:
        n_grid.append([int(n) for n in row])

    if boold:
        print("starting values:")
        pprint.pprint(n_grid)
        print("----")
    octopy_grid = OctopiGrid(n_grid)

    if boold:
        print("----")

    n_steps = 100
    n_flashes = 0
    for n in range(n_steps + 1):
        if boold:
            print("step number", n)
            print(octopy_grid)
            print("total number of flashes:", octopy_grid.n_flashes)
        n_flashes = octopy_grid.n_flashes
        octopy_grid.step()
    
    return n_flashes


def part2(t_input):
    """
    The second part of the puzzle requests after
    how many steps all the Octopus objects do a synchronized flash.

    This function:
    1. parses the input to convert it into a grid of numbers
    2. creates a grid of Octopus objects using an OctopiGrid object
    3. calls octopy_grid.step() to make every Octopus in the OctopiGrid
       "go up" one step until all the Octopus objects are flashing
    4. returns the number of steps it took for all the Octopus objects to flash
    """
    n_grid = []
    for row in t_input:
        n_grid.append([int(n) for n in row])

    octopy_grid = OctopiGrid(n_grid)

    n_steps = 0
    while n_steps < 10000:
        if boold:
            print("step number", n_steps)
            print("all flashing?", octopy_grid.all_flashing)
        if octopy_grid.all_flashing:
            break
        n_steps += 1
        octopy_grid.step()
    
    return n_steps


if __name__ == "__main__":

    try:
        with open("input.txt", "r") as f:
            data_str = f.read()
            data = data_str.splitlines()
            res_1 = part1(data)
            res_2 = part2(data)

            print("=" * 10)
            print("part 1 result (number of flashes):", res_1)
            print("part 2 result (number of steps in which all octopi are flashing):", res_2)

    except FileNotFoundError:
        print("input.txt file doesn't exist. Testing using test_data")
    
    boold = False
    assert part1(test_data) == 1656, "wrong number of flashes"
    assert part2(test_data) == 195, "wrong number of steps"

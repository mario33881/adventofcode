"""
This script finds the least amount of fuel needed
to align vertically a group of submarines 
which have different horizontal coordinates.
"""
import os

input_path = "input.txt"
boold = False
part2 = False  # False -> part 1, True -> part 2


def distance_to_fuel(t_distance, t_const=None):
    """
    Returns the fuel needed to move <t_distance> distance.

    If t_const (constant) is None this is the progression:
    1 -> 1                      -> 1
    2 -> 1 + 2                  -> 3
    3 -> 1 + 2 + 3              -> 6
    4 -> 1 + 2 + 3 + 4          -> 10
    5 -> 1 + 2 + 3 + 4 + 5      -> 15
    6 -> 1 + 2 + 3 + 4 + 5 + 6  -> 21

    If t_const is an integer, each step costs <t_const> fuel
    to move in that direction.

    Example: 
    t_const = 1 means that each step requires 1 fuel
    t_const = 2 means that each step requires 2 fuel
    ...

    :param int t_distance: distance between two points on the same axis
    :param (int, None) t_const: constant value that represents the fuel cost of each movement step
    :return int fuel: amount of fuel needed to move <t_distance> distance
    """
    fuel = 0
    if t_const is None:
        # t_distance + (t_distance - 1) + (t_distance - 2) + ... + 1
        # should have used T(n) = n*(n+1)/2
        for d in range(t_distance, 0, -1):
            fuel += d
    else:
        fuel = t_distance * t_const
    return fuel


if __name__ == "__main__":
    
    if not os.path.isfile(input_path):
        print(input_path, "file doesn't exist")
        exit(1)

    try:
        with open(input_path, "r") as f:
            # crabs_pos = [int(x) for x in "16,1,2,0,4,2,7,1,2,14".strip().split(",")]  # example input
            crabs_pos = [int(x) for x in f.readline().strip().split(",")]
    except ValueError:
        print("couldn't parse input data: NaN found")
        exit(2)

    # prepare a dictionary of fuel sums
    fuel_sums = {}
    for pos in set(crabs_pos):
        fuel_sums[pos] = 0
    
    if boold:
        print("initial fuel counter:")
        print(fuel_sums)
    
    # calculate the fuel necessary to move in one position from every position
    for init_pos in fuel_sums.keys():
        fuel_sum = 0
        for pos in crabs_pos:
            if part2:
                fuel_sum += distance_to_fuel(abs(pos - init_pos))
            else:
                fuel_sum += distance_to_fuel(abs(pos - init_pos), 1)
        
        fuel_sums[init_pos] = fuel_sum
    
    if boold:
        print("fuel counter. each position requires x"
              " amount of fuel for every submarine to reach it")
        print(fuel_sums)

    # find the least amount of fuel needed to move that position    
    min_fuel = next(iter(fuel_sums.values()))
    if boold:
        print("initial value:", min_fuel)
    for pos in fuel_sums.keys():
        if boold:
            print("{} requires {} fuel".format(pos, fuel_sums[pos]))
        if fuel_sums[pos] < min_fuel:
            min_fuel = fuel_sums[pos]

    if part2:
        print("part 2 solution:")
    else:
        print("part 1 solution:")

    print("least amount of fuel is", min_fuel)

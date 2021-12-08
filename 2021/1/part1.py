"""
Counts how many times values contained 
inside the input.txt file increase.
"""
import os

n_increases = 0
filepath = "input.txt"

if __name__ == "__main__":

    if not os.path.isfile(filepath):
        print(filepath, "file doesn't exist")
        exit(1)
    
    with open(filepath, "r") as f:
        line = f.readline()
        while line != "":
            try:
                prev = int(line.strip())
                line = f.readline()
                curr = int(line.strip())

                if curr > prev:
                    n_increases += 1
                    print("depth increased from {} to {}".format(prev, curr))

            except ValueError as e:
                print("Invalid depth value, skipping it...")
                line = f.readline()

    print("---")
    print("Total increases:", n_increases)

"""
Counts if three values summed together result in a value
that is less than the next three values summed together.

Example:
1
22
333
 44
  5

1+2+3 <? 2+3+4 
2+3+4 <? 3+4+5
...
"""
import os

filepath = "input.txt"
n_increases = 0

if __name__ == "__main__":
    
    if not os.path.isfile(filepath):
        print(filepath, "file doesn't exist")
        exit(1)

    with open(filepath, "r") as f:
        lines = [int(line.strip()) for line in f.readlines()]
    
    index = 1
    while index < len(lines) - 2:
        curr_sum = lines[index-1] + lines[index] + lines[index+1]
        next_sum = lines[index] + lines[index+1] + lines[index+2]

        print(lines[index-1], lines[index], lines[index+1])
        print(lines[index], lines[index+1], lines[index+2])
        print("---")
        index += 1

        if curr_sum < next_sum:
            n_increases += 1
    
    print("=" * 10)
    print("Total increases:", n_increases)

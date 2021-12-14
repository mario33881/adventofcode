"""
Measures the  growth rate of lanternfishes.

---

After part 1 I realised that I could use a counter list
to save how many fishes have timer equal to 0, 1, ..., 8

This allowed me to complete the simulation in a short amount of time.
"""
import os

boold = False
days = 256
filepath = "input.txt"

if __name__ == "__main__":
    if not os.path.isfile(filepath):
        print(filepath, "file doesn't exist")
        exit(2)
    
    with open(filepath, "r") as f:
        fishes_string = f.readline().strip()  # fishes_string = "3,4,3,1,2" # example input
    
    try:
        fishes = [int(i) for i in fishes_string.split(",")]
    except ValueError:
        print("Error parsing the input string: input doesn't contain integers")
        exit(1)

    fishes_counter = [0] * 9
    for fish in fishes:
        fishes_counter[fish] += 1
    
    for i in range(days):
        if boold:
            if i == 0:
                print("Initial state: {}".format(fishes_counter))
            else:
                print("After day {}: {}".format(i, fishes_counter))

        zeros = fishes_counter[0]  # this value will be overwritten
        for n in range(len(fishes_counter)-1):
            fishes_counter[n] = fishes_counter[n+1]
        
        fishes_counter[6] += zeros
        fishes_counter[8] = zeros

    print("-" * 10)
    print("After day {} there are {} fishes".format(days, sum(fishes_counter)))

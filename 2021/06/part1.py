"""
Measures the  growth rate of lanternfishes.

---

Since many puzzles were easy to implement using OOP,
I immediately started with creating the Fish class.

This turned out ok for the first part but not for the second one...

This is not an efficient solution and I only realised that in part 2.
"""
import os

boold = False
days = 80
filepath = "input.txt"


class Fish:
    def __init__(self, timer) -> None:
        """
        Represents a fish.

        when self.timer reaches 0, a new fish gets created
        and the current one resets to 6.
        """
        self.timer = timer
    
    def age(self):
        """
        Decrease the timer and return a new fish
        when the current timer goes below zero.
        """
        new_fish = None
        self.timer -= 1

        if self.timer < 0:
            self.timer = 6
            # since the fish is appended to the list, 
            # its timer gets decremented by one in the same day
            # it gets created
            new_fish = Fish(9)  
        
        return new_fish

    def __repr__(self) -> str:
        return str(self.timer)


if __name__ == "__main__":

    if not os.path.isfile(filepath):
        print(filepath, "file doesn't exist")
        exit(2)
    
    with open(filepath, "r") as f:
        fishes_string = f.readline().strip()  # fishes_string = "3,4,3,1,2" # example input
    
    try:
        fishes = [Fish(int(i)) for i in fishes_string.split(",")]
    except ValueError:
        print("Error parsing the input string: input doesn't contain integers")
        exit(1)

    for i in range(days):
        if boold:
            if i == 0:
                print("Initial state: {}".format(fishes))
            else:
                print("After day {}: {}".format(i, fishes))

        for fish in fishes:
            new_fish = fish.age()
            if new_fish is not None:
                fishes.append(new_fish)

    print("-" * 10)
    if boold:
        print("After day {}: {}".format(days, fishes))
    print("After day {} there are {} fishes".format(days, len(fishes)))

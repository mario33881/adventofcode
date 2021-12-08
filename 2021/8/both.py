"""
Four 7 segments displays are incorrectly connected to wires.

This results in patterns that can be used to deduce the correct values.
"""
from itertools import permutations


def read_line_by_line(t_filepath):
    """
    Reads <t_filepath> file and yields one line at a time.
    """
    with open(t_filepath, "r") as f:
        line = f.readline()
        while line != "":
            yield line
            line = f.readline()


def signal_to_digit(t_signal):
    """
    These signals have a unique length that
    permits us to easily know which value the segments represent.

    If the signal has an ambiguos length, return -1.
    """
    digit = -1
    if len(t_signal) == 2:
        # 1
        digit = 1
    elif len(t_signal) == 4:
        # 4
        digit = 4
    elif len(t_signal) == 3:
        # 7
        digit = 7
    elif len(t_signal) == 7:
        # 8
        digit = 8
    
    return digit


def contains_none(t_dict):
    """
    If t_dict contains a value that is None, return True.
    """
    for el in t_dict.values():
        if el is None:
            return True
    
    return False


if __name__ == "__main__":

    digit_counter = [0] * 10  # used for part 1
    output_sum = 0            # used for part 2

    for line in read_line_by_line("input.txt"):
        strip_line = line.strip()
        signals_str = strip_line.split("|")[0]
        output_str = strip_line.split("|")[1]

        signals = signals_str.strip().split(" ")
        output = output_str.strip().split(" ")

        print("Read:", signals, output)

        for signal in output:
            digit = signal_to_digit(signal)

            if digit != -1:
                digit_counter[digit] += 1
        
        # PART 2
        #
        # After studing the length and patterns of each number I've reached the following conclusion.
        #
        # Knowing the combinations of 1, 4, 7, 8 we can find the other combinations:
        #
        # STEP 1: discriminate 0, 6 and 9 (and distinguish them from the other numbers):
        # if length of signal is 6 -> result is one of 0, 6 or 9
        # if the signal contains a combination of 1 -> result is 0 or 9
        #                                 otherwise -> result is 6
        # if the signal contains a combination of 3 -> result is 9
        #                                 otherwise -> result is 0
        #
        # STEP 2: discriminate between 2, 3 and 5:
        # if length of signal is 5 -> result is 2/3/5
        # if the signal contains a combination of 1 -> result is 3
        #                                 otherwise -> result is 2 or 5
        #if adding a segment of the combination of 1 results in 9 -> result is 5
        #                                             otherwise   -> result is 2
        # --> notice that one segment of the 1 combination already needs to be present
        #     for the signal to become a 9 once you add the other segment
        #

        digit_patterns = {
            0: None,
            1: None,
            2: None,
            3: None,
            4: None,
            5: None,
            6: None,
            7: None,
            8: None,
            9: None
        }

        while contains_none(digit_patterns):
            # I need to keep looking until I have all the patterns
            print("Currently I don't know the patterns of these digits: ", end="")
            for pattern in digit_patterns.items():
                if pattern[1] is None:
                    print(pattern[0], ",", end="")
            print("")

            for signal in signals + output:
                if len(signal) in [2, 3, 4, 7]:
                    # I immediately know the digit
                    digit = signal_to_digit(signal)
                    digit_patterns[digit] = ["".join(i) for i in permutations(signal)]
                    print("found pattern of digit:", digit)
                elif len(signal) == 6 and digit_patterns[1] is not None:
                    # it's 0, 6 or a 9 and I know how to make 1 and 3
                    contains_one = False
                    for combination in digit_patterns[1]:
                        # 1 is made of 2 segments that need to be turned on
                        if combination[0] in signal and combination[1] in signal:
                            print(combination, "is inside", signal)
                            contains_one = True
                            break
                    
                    if contains_one:
                        # contains a 1, its a 9 or a 0
                        if  digit_patterns[3] is not None:
                            contains_three = False
                            for combination in digit_patterns[3]:
                                # 3 is made of 5 segments that all need to be turned on
                                if combination[0] in signal \
                                    and combination[1] in signal \
                                    and combination[2] in signal \
                                    and combination[3] in signal \
                                    and combination[4] in signal:
                                    contains_three = True
                                    break
                            
                            if contains_three:
                                # it's 9
                                digit_patterns[9] = ["".join(i) for i in permutations(signal)]
                                print("found pattern of digit:", 9)
                            else:
                                # it's 0
                                digit_patterns[0] = ["".join(i) for i in permutations(signal)]
                                print("found pattern of digit:", 0)
                        else:
                            print("currently I don't know how to make a 3... so I can't distinguish between 0 and 9")
                    else:
                        # doesn't contain a 1, its a 6
                        digit_patterns[6] = ["".join(i) for i in permutations(signal)]
                        print("found pattern of digit:", 6)
                
                elif len(signal) == 5 and digit_patterns[1] is not None:
                    # its 2/3/5 and I know how to make 1 and 9
                    
                    contains_one = False
                    for combination in digit_patterns[1]:
                        # 1 is made of 2 segments that need to be turned on
                        if combination[0] in signal and combination[1] in signal:
                            print(combination, "is inside", signal)
                            contains_one = True
                            break
                    
                    if contains_one:
                        # contains a 1, its a 3
                        digit_patterns[3] = ["".join(i) for i in permutations(signal)]
                        print("found pattern of digit:", 3)
                    else:
                        # it's either 2 or 5
                        if digit_patterns[9] is not None:
                            one_pattern = digit_patterns[1][0]
                            segment1 = one_pattern[0]
                            segment2 = one_pattern[1]
                            
                            # At least one segment of "1" is present in both 2 and 5: 
                            # I need to find the other part and try to "turn it on"
                            # If I add the top right segment to a 5, it becomes a 9
                            # If I add the bottom right segment to a 2, it is not a digit (it's a "reversed 6")
                            if segment1 in signal:
                                mod_signal = signal + segment2
                            else:
                                mod_signal = signal + segment1
                            
                            if mod_signal in digit_patterns[9]:
                                # it's 5
                                digit_patterns[5] = ["".join(i) for i in permutations(signal)]
                                print("found pattern of digit:", 5)
                            else:
                                # it's 2
                                digit_patterns[2] = ["".join(i) for i in permutations(signal)]
                                print("found pattern of digit:", 2)
                        else:
                            print("currently I don't know how to make a 9... so I can't distinguish between 2 and 5")
                else:
                    print("I don't currently know what this is:", signal)

        # now I know every single pattern of this entry (line): I can calculate the output value
        output_value = 0
        for signal in output:
            for digit_pattern in digit_patterns.items():
                if signal in digit_pattern[1]:
                    # I found the digit
                    digit = digit_pattern[0]
                    output_value = output_value * 10 + digit
                    break
        print("Current output value:", output_value)
        output_sum += output_value

    print("Number of 1/4/7/8 (part 1):", sum(digit_counter))
    print("Sum of outputs (part 2):", output_sum)

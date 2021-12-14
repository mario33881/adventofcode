"""
The submarine returns a list of bits that represent status values.

This script allows the user to convert those bits into decimal values.
"""
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


def bits_to_int(t_bits):
    """
    Converts a binary string into an integer.
    """
    less_sig_pos = len(t_bits) - 1

    i = less_sig_pos
    num = 0
    while i >= 0:
        num += (2 ** (less_sig_pos - i)) * int(t_bits[i])
        if boold:
            print("num = 2 ** {} * {} = {}".format(less_sig_pos - i, t_bits[i], (2 ** i) * int(t_bits[i])))
        i -= 1
    if boold:
        print("---")
    return num


def sub_lists(t_a, t_b):
    """
    Subtracts each number in <t_a> by the 
    number in <t_b> that is in the same position
    """
    if not len(t_a) == len(t_b):
        raise ValueError("length should be equal")
    
    res = t_a[:]
    for i in range(len(res)):
        res[i] -= t_b[i]
    
    return res


def create_mask(t_list):
    """
    Creates a mask made of ones in the same position 
    where <t_list> contains numbers >= 0 and zeros
    everywhere else.
    """
    mask = []
    for el in t_list:
        if el >= 0:
            mask.append(1)
        else:
            mask.append(0)
    
    return mask


def count(t_list):
    """
    Counts how many ones and zeros 
    are placed in the same position.
    """
    zeros_counter = None
    ones_counter = None

    for el in t_list:
        bits = [bit for bit in el.strip()]

        if zeros_counter is None:
            zeros_counter = [0 for bit in bits]

        if ones_counter is None:
            ones_counter = [0 for bit in bits]
        
        for i, bit in enumerate(bits):
            if bit == "1":
                ones_counter[i] += 1
            else:
                zeros_counter[i] += 1
    
    return ones_counter, zeros_counter


def filter_lines(t_lines, t_index, t_most):
    """
    Filters lines from <t_lines> by looking
    at the bit in the <t_index> position.

    If <t_most> is True: res will contain
    lines that have in the <t_index> position a 1.

    Otherwise res will contain lines that have a 0
    in the <t_index> position.
    """
    ones_counter, zeros_counter = count(t_lines)

    # subl[0] == ones_counter[0] - zeros_counter[0]
    # subl[1] == ones_counter[1] - zeros_counter[1]
    # ...
    subl = sub_lists(ones_counter, zeros_counter)

    # create a bit mask
    mask = create_mask(subl)

    res = []
    for el in t_lines:
        print(mask, "-", el, "-", t_index)
        if t_most:
            if mask[t_index] == int(el[t_index]):
                res.append(el)
        else:
            if mask[t_index] != int(el[t_index]):
                res.append(el)
    
    return res


if __name__ == "__main__":

    file = "input.txt"
    zeros_counter = None
    ones_counter = None
    for line in read_line_by_line(file):
        bits = [bit for bit in line.strip()]

        if zeros_counter is None:
            zeros_counter = [0 for bit in bits]

        if ones_counter is None:
            ones_counter = [0 for bit in bits]
        
        for i, bit in enumerate(bits):
            if bit == "1":
                ones_counter[i] += 1
            else:
                zeros_counter[i] += 1

    print("ones: ", ones_counter)
    print("zeros:", zeros_counter)

    gamma_bits = ""
    epsilon_bits = ""
    for i in range(len(zeros_counter)):
        if zeros_counter[i] > ones_counter[i]:
            gamma_bits += "0"
            epsilon_bits += "1"
        else:
            gamma_bits += "1"
            epsilon_bits += "0"

    gamma_rate = bits_to_int(gamma_bits)
    epsilon_rate = bits_to_int(epsilon_bits)
    power_consumption = gamma_rate * epsilon_rate
    
    print("gamma_bits =", gamma_bits)
    print("epsilon_bits =", epsilon_bits)
    print("gamma_rate =", gamma_rate)
    print("epsilon_rate =", epsilon_rate)
    print("power_consumption =", power_consumption)

    lines = []
    for line in read_line_by_line(file):
        lines.append(line.strip())

    v_oxygen_bits = lines[:]
    index = 0
    while len(v_oxygen_bits) > 1:
        v_oxygen_bits = filter_lines(v_oxygen_bits, index, t_most=True)
        print(v_oxygen_bits)
        print("-" * 10)
        index += 1

    oxygen_bits = [int(bit) for bit in v_oxygen_bits[0]]
    oxygen_rate = bits_to_int(oxygen_bits)
    print("oxygen rate bits:", oxygen_bits)
    print("oxygen generator rating:", oxygen_rate)

    v_co2_bits = lines[:]
    index = 0
    while len(v_co2_bits) > 1:
        v_co2_bits = filter_lines(v_co2_bits, index, t_most=False)
        print(v_co2_bits)
        print("-" * 10)
        index += 1

    co2_bits = [int(bit) for bit in v_co2_bits[0]]
    co2_rate = bits_to_int(co2_bits)
    print("co2 rate bits:", co2_bits)
    print("co2 scrubber rating:", co2_rate)

    print("life support rating:", co2_rate * oxygen_rate)

"""
The submarine returns a list of bits that represent status values.

This script allows the user to convert those bits into decimal values.
"""
import os

file = "input.txt"
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
    Converts <t_bits> bits to an integer.

    :param str t_bits: string of bits
    :return int num: <t_bits> converted to a number
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


if __name__ == "__main__":

    if not os.path.isfile(file):
        print(file, "file doesn't exist")
        exit(1)
    
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

    print(zeros_counter)
    print(ones_counter)

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

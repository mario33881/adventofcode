"""
Uses a stack to syntax check the input data.
"""

boold = False
test_data = """[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]
"""


class Stack:
    def __init__(self):
        """
        Represents a stack
        """
        self.stack = []

    def push(self, el):
        """
        Appends <el> element to the stack
        """
        self.stack.append(el)

    def pop(self):
        """
        Removes and returns the last stack element
        """
        return self.stack.pop()

      
def get_corrupted_points(t_input):
    """
    The input data contains "corrupted lines":
    these lines have closing parenthesis in wrong places.

    For each corrupted character, for each line,
    this generator yields its "score".
    > Scores are saved in the illegal_scores dictionary.
    """
    illegal_scores = {
            ")": 3,
            "]": 57,
            "}": 1197,
            ">": 25137
    }

    s = Stack()
    for line in t_input.splitlines():
        for el in line:
            if el in ["{", "[", "(", "<"]:
                if el == "{":
                    s.push("}")
                elif el == "[":
                    s.push("]")
                elif el == "(":
                    s.push(")")
                else:
                    s.push(">")
            else:
                rem = s.pop()
                if rem != el:
                    if boold:
                        print("expected '{}', found '{}'".format(rem, el))
                    yield illegal_scores[el]


def get_incomplete_lines(t_input):
    """
    The input data consists of incomplete lines.

    A line is incomplete if some closing parenthesis are missing.

    This generator yields each incomplete line.
    """
    s = Stack()
    for line in t_input.splitlines():
        incomplete = True
        for el in line:
            if el in ["{", "[", "(", "<"]:
                if el == "{":
                    s.push("}")
                elif el == "[":
                    s.push("]")
                elif el == "(":
                    s.push(")")
                else:
                    s.push(">")
            else:
                rem = s.pop()
                if rem != el:
                    # line is corrupted, not incomplete
                    incomplete = False
                    break
        
        if incomplete:
            yield line
                    

def find_closing_chars(t_input):
    """
    Given a list of incomplete lines,
    finds the missing parenthesis
    and calculates a score based on those
    missing parenthesis.
    """
    total_points = []
    char2points = {
        ")": 1,
        "]": 2,
        "}": 3,
        ">": 4
    }
    for line in t_input:
        s = Stack()
        for el in line:
            if el in ["{", "[", "(", "<"]:
                if el == "{":
                    s.push("}")
                elif el == "[":
                    s.push("]")
                elif el == "(":
                    s.push(")")
                else:
                    s.push(">")
            else:
                # removing the parenthesis from the stack
                # because it is already part of the input line
                s.pop()

        # collect from the stack all the missing parenthesis
        line_closing_chars = ""
        for el in s.stack[::-1]:
            line_closing_chars += el
        
        # calculate the line score based on the missing parenthesis
        # and memorize it in total_points
        points = 0
        for char in line_closing_chars:
            points = points * 5 + char2points[char]

        total_points.append(points)
        if boold:
            print("line points:", points)
    
    # find the median score, which is the final score
    sorted_points = sorted(total_points)
    middle_score = sorted_points[len(sorted_points)//2]
    return middle_score


def part1(t_input):
    """
    Uses get_corrupted_points() to get the
    "corrupted score" of each line, adds them together
    and returns the "corrupted score" of the data.
    """
    illegal_points = 0

    for res in get_corrupted_points(t_input):
        illegal_points += res
            
    return illegal_points


def part2(t_input):
    """
    First, get_incomplete_lines() is used to only
    select incomplete lines from the input data.

    Then it uses the find_closing_chars() function
    to calculate the "incomplete score" of the data.
    """
    incomplete_lines = []
    for res in get_incomplete_lines(t_input):
        incomplete_lines.append(res)

    return find_closing_chars(incomplete_lines)


if __name__ == "__main__":

    try:
        with open("input.txt") as f:
            data = f.read()

            print("points part 1:", part1(data))
            print("points part 2:", part2(data))
    except FileNotFoundError:
        print("input file doesnt' exist, testing using test_data")

    boold = False
    assert part1(test_data) == 26397, "Wrong result for test_data, part 1"
    assert part2(test_data) == 288957, "Wrong result for test_data, part 1"

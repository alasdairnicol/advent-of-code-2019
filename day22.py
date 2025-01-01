#!/usr/bin/env python
DECK_SIZE = 10007


def read_input(filename):
    with open(filename) as f:
        return f.read()


def parse_instructions(input_str):
    out = []
    for instruction in input_str.strip().split("\n"):
        if instruction == "deal into new stack":
            function = deal_into_new_stack
            kwargs = {}
        else:
            number = int(instruction.split(" ")[-1])
            if instruction.startswith("deal with increment"):
                function = deal_with_increment
                kwargs = {"increment": number}
            elif instruction.startswith("cut"):
                function = cut
                kwargs = {"n": number}
            else:
                raise ValueError("Unknown instruction: ", instruction)
        out.append((function, kwargs))
    return out


def deal_with_increment(deck, increment):
    order = {increment * x % len(deck): deck[x] for x in range(len(deck))}
    return [order[x] for x in range(len(deck))]


def deal_into_new_stack(deck):
    return list(reversed(deck))


def cut(deck, n):
    return deck[n:] + deck[:n]


def main():
    deck = list(range(DECK_SIZE))

    instructions = parse_instructions(read_input("day22.txt"))
    for function, kwargs in instructions:
        deck = function(deck, **kwargs)
    return deck.index(2019)


if __name__ == "__main__":
    index = main()
    print(index)

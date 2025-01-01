#!/usr/bin/env python
from dataclasses import dataclass
from collections import defaultdict
import math

TRILLION = 1_000_000_000_000


@dataclass
class Reaction:
    output_chemical: str
    output_quantity: int
    input_chemicals: list

    def __str__(self):
        return f"{self.output_quantity} {self.output_chemical}"


def read_input(filename):
    with open(filename) as f:
        return f.readlines()


def parse_reactions(lines):
    reactions = {}
    for line in lines:
        inputs, out = line.rstrip().split("=>")
        out = out.strip()
        inputs = [i.split(" ") for i in inputs.strip().split(", ")]
        inputs = [(int(x), y) for x, y in inputs]
        output_quantity, output_chemical = out.split(" ")
        output_quantity = int(output_quantity)
        reaction = Reaction(output_chemical, output_quantity, inputs)
        reactions[output_chemical] = reaction
    return reactions


def main():
    reactions = parse_reactions(read_input("day14.txt"))
    target = TRILLION

    min_ore, max_ore = None, None
    guess = 1

    count = 0

    while min_ore is None or max_ore is None or min_ore < max_ore:
        print(min_ore, guess, max_ore)
        ore = ore_required(reactions, guess)
        if ore <= target:
            min_ore = guess
        elif ore > target:
            max_ore = guess
        if max_ore is None:
            guess = guess * 2
        else:
            guess = (min_ore + max_ore) // 2
            if guess == min_ore:
                assert min_ore == max_ore - 1
                return guess
        count += 1

        # Prevent infinite loop
        if count == 100:
            print("Breaking after %s rounds" % count)
            break


def ore_required(reactions, fuel):
    required = defaultdict(int)
    required["FUEL"] = fuel
    ore = 0

    excess = defaultdict(int)

    while required:
        for key in list(required):
            quantity, output = required.pop(key), key
            reaction = reactions[output]
            multiplier = math.ceil(
                (quantity - excess.get(key, 0)) / reaction.output_quantity
            )
            excess[key] += multiplier * reaction.output_quantity - quantity
            for x, y in reaction.input_chemicals:
                if y == "ORE":
                    ore += x * multiplier
                else:
                    required[y] += x * multiplier

    return ore


if __name__ == "__main__":
    ore = main()
    print(ore)

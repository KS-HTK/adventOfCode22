# -*- coding: utf-8 -*-

"""Basic Python file for each day"""
from typing import List

input: List[str] = None
# TODO: change the path of input file!
with open('day01/input', 'r', encoding='utf-8') as f:
  input = map(lambda s: s.strip(), f.readlines())

numbers: List[int] = list(map(int, input))

# Part 1:
def part1(input=None):
  pass

# Part 2:
def part2(input=None):
  pass


if __name__ == "__main__":
  print("Part 1:", part1(numbers))
  print("Part 2:", part2(numbers))
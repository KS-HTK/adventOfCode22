# -*- coding: utf-8 -*-

from typing import List

# Part 1:
def part1(input: str = None) -> int:
  return find_first_unique_substr(input)

# Part 2:
def part2(input: str = None) -> int:
  return find_first_unique_substr(input, 14)

def find_first_unique_substr(input, l: int = 4) -> int:
  for i in range(len(input)):
    if i < l-1:
      continue
    if len(''.join(set(input[i-l+1:i+1]))) == l:
      return i+1

def get_input():
  with open('day06/input', 'r', encoding='utf-8') as f:
    input = f.read().rstrip()
  return input

if __name__ == "__main__":
  input = get_input()
  print("Part 1:", part1(input))
  print("Part 2:", part2(input))
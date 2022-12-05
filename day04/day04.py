# -*- coding: utf-8 -*-

from typing import List

input = None
with open('day04/input', 'r', encoding='utf-8') as f:
  input = f.read().rstrip().split('\n')
input = list(map(lambda s: s.strip().split(','), input))
input = list(map(lambda l: list(map(lambda s: s.split('-'), l)), input))
input = [[[int(j) for j in i] for i in x] for x in input]


def solve(input: List[List[List[int]]], func):
  res: int = 0
  for lst in input:
    if func(lst[0], lst[1]) or func(lst[1], lst[0]):
      res += 1
  return res


def range_subset([x1, x2]: List[int], [y1, y2]: List[int]):
  return x1 <= y1 and y2 <= x2


def range_overlap([x1, x2]: List[int], [y1, y2]: List[int]):
  return x1 <= y2 and y1 <= x2


if __name__ == "__main__":
    print("Part 1:", solve(input, range_subset))
    print("Part 2:", solve(input, range_overlap))

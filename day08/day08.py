# -*- coding: utf-8 -*-

from typing import List
from math import prod

# Part 1:
def part1(input: List[List[int]]) -> int:
  visible: int = 0
  for y, a in enumerate(input):
    for x, b in enumerate(a):
      # Up
      seen: bool = True
      i = y-1
      while i >= 0:
        if b <= input[i][x]:
          seen = False
          break
        i -= 1
      if seen:
        visible += 1
        continue
      # Down
      seen = True
      i = y+1
      while i < len(input):
        if b <= input[i][x]:
          seen = False
          break
        i += 1
      if seen:
        visible += 1
        continue
      # Left
      seen = True
      i = x-1
      while i >= 0:
        if b <= a[i]:
          seen = False
          break
        i -= 1
      if seen:
        visible += 1
        continue
      # Right
      seen = True
      i = x+1
      while i < len(a):
        if b <= a[i]:
          seen = False
          break
        i += 1
      if seen:
        visible += 1
  return visible

# Part 2:
def part2(input: List[List[int]]) -> int:
  max_seenic_score: int = 0
  for y, a in enumerate(input):
    for x, b in enumerate(a):
      distance: List[int] = [0, 0, 0, 0]
      # Up
      i = y-1
      while i >= 0 and b > input[i][x]:
        i -= 1
      distance[0] = y-i-1
      # Down
      i = y+1
      while i < len(input) and b > input[i][x]:
        i += 1
      distance[1] = i-y-1
      # Left
      i = x-1
      while i >= 0 and b > a[i]:
        i -= 1
      distance[2] = x-i # not to sure why -1 not required here
      # Right
      i = x+1
      while i < len(a) and b > a[i]:
        i += 1
      distance[3] = i-x-1
      max_seenic_score = max(prod(distance), max_seenic_score)
  return max_seenic_score

def get_input():
  with open('day08/input', 'r', encoding='utf-8') as f:
    input = [[int(c) for c in s.strip()] for s in f.read().rstrip().split('\n')]
  return input

if __name__ == "__main__":
  input = get_input()
  print("Part 1:", part1(input))
  print("Part 2:", part2(input))
# -*- coding: utf-8 -*-

from typing import List, Callable

input = None
with open('day01/input', 'r', encoding='utf-8') as f:
  input = f.read()
input = input.rstrip().split('\n\n')
elf: List[List[int]] = [list(map(lambda x: int(x), s.split('\n'))) for s in input]

# Part 1:
def part1(input: List[List[int]]=None) -> int:
  max: int = 0
  for c in input:
    if c > max:
      max = c
  return max


# Part 2:
def part2(input: List[int]=None) -> int:
  max: int = 0
  sec: int = 0
  thi: int = 0
  for c in input:
    if c > max:
      thi = sec
      sec = max
      max = c
    elif c > sec:
      thi = sec
      sec = c
    elif c > thi:
      thi = c
  return max+sec+thi

if __name__ == "__main__":
  print("Part 1:", part1([sum(x) for x in elf]))
  print("Part 2:", part2([sum(x) for x in elf]))
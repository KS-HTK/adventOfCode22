# -*- coding: utf-8 -*-

from typing import List
from time import perf_counter

def profiler(method):
  def profiler_method(*arg, **kw):
    t = perf_counter()
    ret = method(*arg, **kw)
    print(f'{method.__name__} method took : {perf_counter()-t:.4f} sec')
    return ret
  return profiler_method

input: List[str] = None
with open('day03/input', 'r', encoding='utf-8') as f:
  input = f.read().rstrip()
  input = input.split('\n')
  input = list(map(lambda s: s.strip(), input))

# Part 1:
def part1(input: List[str]=None):
  score: int = 0
  for line in input:
    sl1: slice = slice(0, int(len(line)/2))
    sl2: slice = slice(int(len(line)/2), len(line))
    s1: str = line[sl1]
    s2: str = line[sl2]
    for letter in s1:
      if letter in s2:
        score += get_prio(letter)
        break
  return score

# Part 2:
def part2(input: List[str]=None):
  score: int = 0
  i: int = 0
  while i < len(input):
    r1: str = input[i]
    r2: str = input[i+1]
    r3: str = input[i+2]
    for letter in r1:
      if letter in r2 and letter in r3:
        score += get_prio(letter)
        break
    i+=3
  return score

def get_prio(char: str) -> int:
  ordn = ord(char)
  return ordn-38 if ordn < 97 else ordn-96

@profiler
def solve():
  print("Part 1:", part1(input))
  print("Part 2:", part2(input))

if __name__ == "__main__":
  solve()

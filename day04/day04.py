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

def get_input():
  input = None
  with open('day04/input', 'r', encoding='utf-8') as f:
    input = f.read().rstrip().split('\n')
  input = list(map(lambda s: s.strip().split(','), input))
  input = list(map(lambda l: list(map(lambda s: s.split('-'), l)), input))
  input = [[[int(j) for j in i] for i in x] for x in input]
  return input

def _solve(input: List[List[List[int]]], func):
  res: int = 0
  for lst in input:
    if func(*lst[0], *lst[1]) or func(*lst[1], *lst[0]):
      res += 1
  return res

def range_subset(x1: int, x2: int, y1: int, y2: int):
  return x1 <= y1 and y2 <= x2

def range_overlap(x1: int, x2: int, y1: int, y2: int):
  return x1 <= y2 and y1 <= x2

@profiler
def solve():
  input = get_input()
  print("Part 1:", _solve(input, range_subset))
  print("Part 2:", _solve(input, range_overlap))

if __name__ == "__main__":
  solve()

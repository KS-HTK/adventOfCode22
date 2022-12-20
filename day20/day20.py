# -*- coding: utf-8 -*-

import os
from time import perf_counter
from typing import List, Tuple

# Global variables
# lookup[index] = original_index
#  This might seem inverse, but it makes updating the list easier
lookup: List[int] = []

def profiler(method):
  def profiler_method(*arg, **kw):
    t = perf_counter()
    ret = method(*arg, **kw)
    print(f'{method.__name__} method took : {perf_counter()-t:.4f} sec')
    return ret
  return profiler_method

# Part 1:
def part1(content: List[int]) -> int:
  global lookup
  lookup = [i for i in range(len(content))] # reset lookup
  return find_coords(mix(content))

# Part 2:
def part2(content: List[int]) -> int:
  global lookup
  lookup = [i for i in range(len(content))] # reset lookup
  for _ in range(10):
    content = mix(content)
  return find_coords(content)

def mix(content: List[int]) -> List[int]:
  global lookup
  for i in range(len(content)):
    pos = lookup.index(i)
    # move num and its
    num = content.pop(pos)
    ind = lookup.pop(pos)
    n_ind = (pos+num) % len(content)
    if n_ind == 0:
      n_ind = len(content)
    content.insert(n_ind, num)
    lookup.insert(n_ind, ind)
  return content

def find_coords(content: List[int]) -> int:
  # search for value 0
  ind = content.index(0)
  return sum([content[(ind+i*1000)%len(content)] for i in range(1,4)])

def get_input() -> Tuple[List[int], List[int]]:
  content1: List[int] = []
  content2: List[int] = []
  with open(os.path.dirname(os.path.realpath(__file__))+'/input', 'r', encoding='utf-8') as f:
    for s in f.read().rstrip().split('\n'):
      v = int(s.strip())
      content1.append(v)
      content2.append(v * 811589153)
  return content1, content2

@profiler
def solve():
  content1, content2 = get_input()
  print("Part 1:", part1(content1))
  print("Part 2:", part2(content2))

if __name__ == "__main__":
  solve()
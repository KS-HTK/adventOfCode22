# -*- coding: utf-8 -*-

import os
from time import perf_counter
from typing import List, Tuple

def profiler(method):
  def profiler_method(*arg, **kw):
    t = perf_counter()
    ret = method(*arg, **kw)
    print(f'{method.__name__} method took : {perf_counter()-t:.4f} sec')
    return ret
  return profiler_method

# Part 1:
def part1(content = None) -> int:
  content = mix(content)
  return find_coords(content)

# Part 2:
def part2(content = None) -> int:
  for _ in range(10):
    content = mix(content)
  return find_coords(content)

def mix(content: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
  for i in range(len(content)):
    # find (i, _) in content
    ind = 0
    while True:
      if content[ind][0] == i:
        break
      ind += 1
    # move content[ind]
    content = move(ind, content)
  return content

def find_coords(content: List[Tuple[int, int]]) -> int:
  ind = 0
  while True:
    if content[ind][1] == 0:
      break
    ind += 1

  # find coords
  k1 = (ind+1000)%len(content)
  k2 = (ind+2000)%len(content)
  k3 = (ind+3000)%len(content)
  return content[k1][1]+content[k2][1]+content[k3][1]


def move(pos: int, arr: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
  ind, num = arr.pop(pos)
  n_ind = (pos+num)%len(arr)
  if n_ind == 0:
    n_ind = len(arr)
  arr.insert(n_ind, (ind, num))
  return arr

def get_input():
  with open(os.path.dirname(os.path.realpath(__file__))+'/input', 'r', encoding='utf-8') as f:
    content = [(i, int(s.strip())) for i, s in enumerate(f.read().rstrip().split('\n'))]
  content2 = [(i, n * 811589153) for i, n in content]
  return content, content2

@profiler
def solve():
  content, content2 = get_input()
  print("Part 1:", part1(content))
  print("Part 2:", part2(content2))

if __name__ == "__main__":
  solve()
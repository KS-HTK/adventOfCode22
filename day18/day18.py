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
def part1(cubes: List[Tuple[int, int, int]]) -> int:
  return sum([len(list([d for d in gen_neighbors(*c) if d not in cubes])) for c in cubes])

# Part 2:
def part2(cubes: List[Tuple[int, int, int]]) -> int:
  _min = min([d for c in cubes for d in c])
  _max = max([d for c in cubes for d in c])

  trapped = set()
  for x in range(_min, _max+1):
    for y in range(_min, _max+1):
      for z in range(_min, _max+1):
        if is_trapped((x, y, z), cubes, _min, _max):
          trapped.add((x, y, z))
  
  surface = 0
  for c in cubes:
    for n in gen_neighbors(*c):
      if n not in cubes and n not in trapped:
        surface += 1

  return surface
  
def is_trapped(c, cube_set, _min, _max):
    queue = []
    visited = set()
    def add(key):
        if key not in visited and key not in cube_set:
            visited.add(key)
            queue.append(key)
    add(c)
    while queue:
        c = queue.pop(0)
        if min(*c) < _min or max(*c) > _max:
            return False
        for n in gen_neighbors(*c):
            add(n)
    return True

def gen_neighbors(x, y, z: Tuple[int, int, int]):
  yield (x+1, y, z)
  yield (x-1, y, z)
  yield (x, y+1, z)
  yield (x, y-1, z)
  yield (x, y, z+1)
  yield (x, y, z-1)

def get_input() -> List[Tuple[int, int, int]]:
  with open(os.path.dirname(os.path.realpath(__file__))+'/input', 'r', encoding='utf-8') as f:
    content = [list(map(int, s.strip().split(','))) for s in f.read().rstrip().split('\n')]
  content = [(x, y, z) for x, y, z in content]
  return content

@profiler
def solve():
  content = get_input()
  print("Part 1:", part1(content))
  print("Part 2:", part2(content))

if __name__ == "__main__":
  solve()
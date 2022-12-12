# -*- coding: utf-8 -*-

import os
from time import perf_counter
from typing import List, Dict, Tuple

def profiler(method):
    def profiler_method(*arg, **kw):
        t = perf_counter()
        ret = method(*arg, **kw)
        print(f'{method.__name__} method took : {perf_counter()-t:.4f} sec')
        return ret
    return profiler_method

def find_paths(grid: Dict[complex, str], start: complex, end: complex) -> Dict[complex, int]:
  shortest_paths = {end: 0}
  queue = [end]

  while queue:
    p1 = queue.pop(0)
    for p2 in [p1-1, p1+1, p1-1j, p1+1j]:
      if not p2 in shortest_paths and move_valid(grid, p1, p2):
        shortest_paths[p2] = shortest_paths[p1]+1
        queue.append(p2)

  return shortest_paths

def move_valid(grid, p1, p2):
  return (p2 in grid and
    ((grid[p1] == 'E' and grid[p2] in 'yz') or
    (grid[p2] == 'S' and grid[p1] in 'ab') or
    ord(grid[p1]) - ord(grid[p2]) <= 1))

def get_input():
  with open(os.path.dirname(os.path.realpath(__file__))+'/input', 'r', encoding='utf-8') as f:
    content = [[l for l in s.strip()] for s in f.read().rstrip().split('\n')]
  return content

@profiler
def solve():
  content = get_input()
  grid = {x + y * 1j: e for y, line in enumerate(content)
                        for x, e in enumerate(line)}
  start = [k for k, v in grid.items() if v == 'S'][0]
  end = [k for k, v in grid.items() if v == 'E'][0]
  paths = find_paths(grid, start, end)
  print("Part 1:", paths[start])
  print("Part 2:", sorted(paths[p] for p in paths if grid[p] in 'Sa')[0])

if __name__ == "__main__":
  solve()
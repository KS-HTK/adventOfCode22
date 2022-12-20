# -*- coding: utf-8 -*-

import os
import re
from time import perf_counter
from typing import List, Tuple

def profiler(method):
  def profiler_method(*arg, **kw):
    t = perf_counter()
    ret = method(*arg, **kw)
    print(f'{method.__name__} method took : {perf_counter()-t:.4f} sec')
    return ret
  return profiler_method

def part1(content: List[Tuple[int, int, int]]) -> int:
  TARGET_Y: int = 2000000
  xl: int = 40000000
  xh: int = -40000000
  for sx, sy, md in content:
    dx: int = md - int(abs(TARGET_Y - sy))
    if dx > 0:
      xl = min(xl, int(sx - dx))
      xh = max(xh, int(sx + dx))
  return xh - xl

# Part 2:
def part2(content: List[Tuple[int, int, int]]) -> int:
  sign = lambda x: x // abs(x) if x != 0 else 0
  for sx, sy, mds in content:
    for tx, ty, mdt in content:
      md = int(abs(sx - tx) + abs(sy - ty))
      if md == mds+mdt+2:
        dirx = sign(tx - sx)
        for p in range(mds+1):
          ux = sx + dirx * (mds + 1) + -1 * dirx * p
          uy = sy + sign(ty - sy) * p
          if (all(abs(ux - vx) + abs(uy - vy) > mdv for vx, vy, mdv in content)):
            return int(ux * 4000000 + uy)

def get_input(suffix=''):
  with open(os.path.dirname(os.path.realpath(__file__))+'/input'+suffix, 'r', encoding='utf-8') as f:
    content = [s.strip() for s in f.read().rstrip().split('\n')]
  ints = [list(map(int, re.findall("-?\d+", l))) for l in content]
  return [(l[0], l[1], int(abs(l[0]-l[2])+abs(l[1]-l[3]))) for l in ints]

@profiler
def solve():
  content: List[Tuple[complex, int]] = get_input()
  print("Part 1:", part1(content))
  print("Part 2:", part2(content))

# Alternative solution for part 1 & 2: !!!! SLOW !!!!
# we will render each line as a string and then search for the '#.#' pattern
# ONLY WORKS FOR THE EXAMPLE INPUT
@profiler
def solve2() -> None:
  sensors: List[Tuple[int, int, int]] = get_input('.txt')
  TARGET_Y: int = 10
  xy_max: int = 0
  for sx, sy, md in sensors:
    xy_max = max(xy_max, abs(sx+md), abs(sx-md), abs(sy+md), abs(sy-md))
  xy_max+=1
  grid: Dict[int, str] = dict()
  for y in range(-xy_max, xy_max):
    grid[y] = (''.join(['#' if any(abs(x - sx) + abs(y - sy) <= md for sx, sy, md in sensors) else '.' for x in range(-xy_max, xy_max)]))
  dot_line = (''.join(['.' for _ in range(-xy_max, xy_max)]))
  while dot_line in grid.values():
    grid.pop([k for k, v in grid.items() if v == dot_line][0])
  min_x: int = min([l.index('#') for l in grid.values()])
  max_x: int = max([l.rindex('#') for l in grid.values()])
  grid: Dict[int, str] = {y: l[min_x:max_x+1] for y, l in grid.items()} 
  print("Part 1:", grid[TARGET_Y].count('#')-1) # -1 because there is a beacon in y=10
  # find the '.' surrounded by '#' in the grid
  for y, l in grid.items():
    if '#.#' in l:
      x = grid[y].index('#.#')+1
      if grid[y-1][x] == '#' and grid[y+1][x] == '#':
        print("Part 2:", (x+min_x-xy_max) * 4000000 + y)
        break
  print('\n'.join([''.join(l) for l in grid.values()]))

if __name__ == "__main__":
  solve()
  #solve2()
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

def get_input():
  with open(os.path.dirname(os.path.realpath(__file__))+'/input', 'r', encoding='utf-8') as f:
    content = [s.strip() for s in f.read().rstrip().split('\n')]
  ints = [list(map(int, re.findall("-?\d+", l))) for l in content]
  return [(l[0], l[1], int(abs(l[0]-l[2])+abs(l[1]-l[3]))) for l in ints]

@profiler
def solve():
  content: List[Tuple[complex, int]] = get_input()
  print("Part 1:", part1(content))
  print("Part 2:", part2(content))

if __name__ == "__main__":
  solve()
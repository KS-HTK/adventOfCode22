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

def part1(content: List[Tuple[complex, int]]) -> int:
  TARGET_Y = 2000000
  xl: int = 40000000
  xh: int = -40000000
  for s, md in content:
    dx: int = md - int(abs(TARGET_Y - s.imag))
    if dx > 0:
      xl = min(xl, int(s.real - dx))
      xh = max(xh, int(s.real + dx))
  return xh - xl

# Part 2:
def part2(content: List[List[complex]]) -> int:
  for s, md in content:
    for p in range(md + 1):
      for tx, ty in ((s.real - md - 1 + p, s.imag - p),
                     (s.real + md + 1 - p, s.imag - p),
                     (s.real - md - 1 + p, s.imag + p),
                     (s.real + md + 1 - p, s.imag + p)):
        if (0 <= tx <= 4000000 and
            0 <= ty <= 4000000 and
            all(abs(tx - s2.real) + abs(ty - s2.imag) > md2
                for s2, md2 in content)):
          return int(tx * 4000000 + ty)

def get_input():
  with open(os.path.dirname(os.path.realpath(__file__))+'/input', 'r', encoding='utf-8') as f:
    content = [s.strip() for s in f.read().rstrip().split('\n')]
  ints = [list(map(int, re.findall("-?\d+", l))) for l in content]
  c = lambda x, y: complex(x, y)
  return [(c(l[0], l[1]), int(abs(l[0]-l[2])+abs(l[1]-l[3]))) for l in ints]

@profiler
def solve():
  content = get_input()
  print("Part 1:", part1(content)) # 5083287
  print("Part 2:", part2(content)) # 13134039205729

if __name__ == "__main__":
  solve()
# -*- coding: utf-8 -*-

import os
from time import perf_counter
from typing import Set

def profiler(method):
  def profiler_method(*arg, **kw):
    t = perf_counter()
    ret = method(*arg, **kw)
    print(f'{method.__name__} method took : {perf_counter()-t:.4f} sec')
    return ret
  return profiler_method

def sandflow(blocked: Set[complex], abyss: int = 0) -> str|int:
  p1 = None
  t = 0
  while 500 not in blocked:
    s = 500
    while True:
      if s.imag >= abyss:
        if not p1:
          p1 = t
        break
      if s + 1j not in blocked:
        s += 1j
      elif s + 1j - 1 not in blocked:
        s += 1j - 1
      elif s + 1j + 1 not in blocked:
        s += 1j + 1
      else:
        break
    blocked.add(s)
    t += 1
  return p1, t

def get_input():
  with open(os.path.dirname(os.path.realpath(__file__))+'/input', 'r', encoding='utf-8') as f:
    content = [[list(map(int, r.split(','))) for r in s.strip().split(' -> ')] for s in f.read().rstrip().split('\n')]
  return content

@profiler
def solve():
  content = get_input()
  blocked = set()
  abyss = 0
  for ln in content:
    for (x1, y1), (x2, y2) in zip(ln, ln[1:]):
      x1, x2 = sorted([x1, x2])
      y1, y2 = sorted([y1, y2])
      for x in range(x1, x2+1):
        for y in range(y1, y2+1):
          blocked.add(x+y*1j)
          abyss = max(abyss, y+1)

  print('Part 1: %s\nPart 2: %s' % sandflow(blocked, abyss))

if __name__ == "__main__":
  solve()
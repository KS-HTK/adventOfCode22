# -*- coding: utf-8 -*-

import os
from time import perf_counter
from typing import List

def profiler(method):
  def profiler_method(*arg, **kw):
    t = perf_counter()
    ret = method(*arg, **kw)
    print(f'{method.__name__} method took : {perf_counter()-t:.4f} sec')
    return ret
  return profiler_method

def snafu_to_int(snafu: str) -> int:
  num = 0
  for i, x in enumerate(snafu[::-1]):
    if x == '-':
      d = -1
    elif x == '=':
      d = -2
    else:
      d = int(x)
    num += d*(5**i)
  return num

def to_snafu(num: int) -> str:
  s = ""
  while num:
    d = (num%5)
    if d == 4:
      s = '-' + s
      num+=1
    elif d == 3:
      s = '=' + s
      num+=2
    else:
      s = str(d) + s
    num //= 5
  return s

def get_input() -> List[int]:
  with open(os.path.dirname(os.path.realpath(__file__))+'/input', 'r', encoding='utf-8') as f:
    nums = [snafu_to_int(s.strip()) for s in f.read().rstrip().split('\n')]
  return nums

@profiler
def solve() -> None:
  nums: List[int] = get_input()
  print("Part 1:", to_snafu(sum(nums)))

if __name__ == "__main__":
  solve()
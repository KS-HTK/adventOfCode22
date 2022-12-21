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

with open('day05/input', 'r', encoding='utf-8') as f:
  [start, steps] = f.read().rstrip().split('\n\n')
steps = [s.lstrip('move ') for s in steps.split('\n')]
steps = [[[int(x) for x in s.split(' to ')] for s in l.split(' from ')] for l in steps]

# Part 1:
def part1(s: List[List[str]], steps: List[List[int]]) -> str:
  for [[c], [f, t]] in steps:
    if len(s[f-1]):
      tmp = s[f-1][-c:]
      tmp.reverse()
      s[t-1].extend(tmp)
      del s[f-1][-c:]
  return get_top_crates(s)

# Part 2:
def part2(s: List[List[str]], steps: List[List[int]]) -> str:
  for [[c], [f, t]] in steps:
    if len(s[f-1]):
      s[t-1].extend(s[f-1][-c:])
      del s[f-1][-c:]
  return get_top_crates(s)

def get_top_crates(config: List[List[str]]) -> str:
  rtn: str = ''.join([s.pop() for s in config]) 
  return rtn

def parse_startconfig(input: str) -> List[List[str]]:
  input = input.splitlines()
  cols = input.pop().rsplit()
  col_count = int(cols.pop())
  input.reverse()
  startconfig = [[] for _ in range(col_count)]
  for line in input:
    for i in range(col_count):
      if line[1+i*4]!=' ':
        startconfig[i].append(line[1+i*4])
  return startconfig

@profiler
def solve():
  startconfig: List[List[str]] = parse_startconfig(start)
  print("Part 1:", part1([s[:] for s in startconfig], steps))
  print("Part 2:", part2([s[:] for s in startconfig], steps))

if __name__ == "__main__":
  solve()

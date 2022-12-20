# -*- coding: utf-8 -*-

from typing import List, Set
from math import prod
from time import perf_counter

def profiler(method):
  def profiler_method(*arg, **kw):
    t = perf_counter()
    ret = method(*arg, **kw)
    print(f'{method.__name__} method took : {perf_counter()-t:.4f} sec')
    return ret
  return profiler_method

# Part 1:
def part1(height: List[List[int]]) -> int:
  visible: Set[(int, int)] = set()
  # This code is inspired by glor8 js code. 
  #  For my original version see prior commit.
  for y, line in enumerate(height): # iterate t -> d
    lr = rl = -1
    for x in range(len(line)): # iterate l -> r
      nx = (len(line)-1)-x #index from end
      if lr < line[x]: #l->r
        visible.add((x, y))
        lr = line[x]
      if rl < line[nx]: #r->l
        visible.add((nx, y))
        rl = line[nx]
  # assert that all lists in list are equal lenght
  assert len(set([len(l) for l in height])) == 1 
  for x in range(len(height[0])): # iterate l -> r
    tb = bt = -1
    for y in range(len(height)): # iterate t -> d
      ny = (len(height)-1)-y #index from end
      if tb < height[y][x]: #t->b
        visible.add((x, y))
        tb = height[y][x]
      if bt < height[ny][x]: #b->t
        visible.add((x, ny))
        bt = height[ny][x]
  return len(visible)

# Part 2:
def part2(height: List[List[int]]) -> int: # 405769
  max_seenic_score: int = 0
  assert len(height) == len(height[0])
  lenh = max(len(height), len(height[0]))
  for y in range(lenh):
    for x in range(lenh):
      h = height[y][x]
      # t, b, l, r
      visible_trees: List[int] = [0, 0, 0, 0]
      view: List[bool] = [True, True, True, True]
      i = 1
      while True:
        # -> t
        if view[0] and y-i >= 0:
          visible_trees[0] += 1
        if y-i < 0 or height[y-i][x] >= h:
          view[0] = False
        # -> b
        if view[1] and y+i < lenh:
          visible_trees[1] += 1
        if y+i >= lenh or height[y+i][x] >= h:
          view[1] = False
        # -> l
        if view[2] and x-i >= 0:
          visible_trees[2] += 1
        if x-i < 0 or height[y][x-i] >= h:
          view[2] = False
        # -> r
        if view[3] and x+i < lenh:
          visible_trees[3] += 1
        if x+i >= lenh or height[y][x+i] >= h:
          view[3] = False
        if True not in view:
          break
        i += 1
      max_seenic_score = max(prod(visible_trees), max_seenic_score)
  return max_seenic_score

def get_input():
  with open('day08/input', 'r', encoding='utf-8') as f:
    input = [[int(c) for c in s.strip()] for s in f.read().rstrip().split('\n')]
  return input

def solve():
  input = get_input()
  print("Part 1:", part1(input))
  print("Part 2:", part2(input))

if __name__ == "__main__":
  solve()

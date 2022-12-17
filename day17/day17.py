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

# Constants
ROCKS = [ # from bottom to top
  [0b0011110],
  [0b0001000,0b0011100,0b0001000],
  [0b0011100,0b0000100,0b0000100],
  [0b0010000,0b0010000,0b0010000,0b0010000],
  [0b0011000,0b0011000],
]
PT1_ROCKS = 2022
PT2_ROCKS = 1000000000000

# Part 1 & 2:
def build_tower() -> int:
  jet_seq = get_input()
  jet_index = 0
  tower: List[int] = []
  truncated = 0
  pt1_hight = 0
  pt2_hight = 0
  cycle: Dict[(int, int), int] = {}
  cyc_rock = None
  cyc_tower_hight = None
  # first rock
  rock = 0
  rock_hight = len(tower) + 3
  rock_shape = list(ROCKS[rock%len(ROCKS)])
  while rock < PT2_ROCKS:
    # shift rock left or right
    if jet_seq[jet_index]: # '<'
      # verify no wall collision occures
      # and verify no rock collision occures
      if (all([rock_shape[i] & (1<<6) == 0 for i in range(len(rock_shape))]) and
          all([(rock_shape[i]<<1) & tower[rock_hight+i] == 0 
                for i in range(len(rock_shape)) if rock_hight+i < len(tower)])):
          rock_shape = [bn << 1 for bn in rock_shape]
    else: # '>'
      if (all([rock_shape[i] & 1 == 0 for i in range(len(rock_shape))]) and 
          all([(rock_shape[i]>>1) & tower[rock_hight+i] == 0
                for i in range(len(rock_shape)) if rock_hight+i < len(tower)])):
          rock_shape = [bn >> 1 for bn in rock_shape]
    jet_index += 1
    jet_index %= len(jet_seq)
    
    # save pt1_hight
    if rock == PT1_ROCKS:
      pt1_hight = len(tower)+truncated
      if pt2_hight != 0:
        return pt1_hight, pt2_hight
    # shift rock down
    if (rock_hight > 0 and (rock_hight > len(tower)
        or all([rock_shape[i] & tower[rock_hight+i-1] == 0
                for i in range(len(rock_shape)) if rock_hight+i-1 < len(tower)]))):
      rock_hight -= 1
    else:
      # add rock to tower
      for i in range(len(rock_shape)):
        if rock_hight+i < len(tower):
          tower[rock_hight+i] |= rock_shape[i]
        else:
          tower.append(rock_shape[i])
      # Optimization:
      # turncate tower
      blocked = 0
      for i in range(len(tower)-1, 0, -1):
        if blocked == 0b1111111:
          tower = tower[i:]
          truncated += i
          break
        blocked |= tower[i]
      # get new rock:
      rock += 1
      rock_hight = len(tower) + 3
      rock_shape = list(ROCKS[rock%len(ROCKS)])
      # Optimization:
      # Cycle detection (The cicle in my input is only at second time a match occures)
      #  - pt1_hight ensures no premature cycle detection
      shape = rock%len(ROCKS)
      if (jet_index, shape) in cycle and pt1_hight != 0:
        cyc_rock = rock - cycle[(jet_index, shape)][ 0 ]
        cyc_tower_hight = len(tower)+truncated - cycle[(jet_index, shape)][ 1 ]
      cycle[(jet_index, shape)] = (rock, len(tower)+truncated)
      if cyc_tower_hight and cyc_rock and (1000000000000 - rock) % cyc_rock == 0:
        pt2_hight = len(tower)+truncated + (1000000000000 - rock) // cyc_rock * cyc_tower_hight
        if pt1_hight != 0:
          return pt1_hight, pt2_hight
  return pt1_hight, pt2_hight

# Visualization function used for debugging
def visualize_tower(tower: List[int], rock_hight: int, rock_shape: List[int]) -> None:
  for i in range(rock_hight+len(rock_shape)-1, -1, -1):
    if i >= rock_hight and i < len(tower):
      print(f'{tower[i]|rock_shape[i-rock_hight]:07b}'.replace('0', '.'))
    elif i >= rock_hight:
      print(f'{rock_shape[i-rock_hight]:07b}'.replace('1', '#').replace('0', '.'))
    elif i < len(tower):
      print(f'{tower[i]:07b}'.replace('1', '#').replace('0', '.'))
    else:
      print(f'{0:07b}'.replace('0', '.'))
  print()

def get_input():
  with open(os.path.dirname(os.path.realpath(__file__))+'/input.txt', 'r', encoding='utf-8') as f:
    content = [s == '<' for s in f.read().rstrip()]
  return content

@profiler
def solve():
  print("Part 1: %d\nPart 2: %d" % build_tower())
  #Part 1: 3083 (3068)
  #Part 2: 1532183908048 (1514285714288)

if __name__ == "__main__":
  solve()
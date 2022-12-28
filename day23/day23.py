# -*- coding: utf-8 -*-

import os
from time import perf_counter
from typing import List, Dict, Tuple, Generator, Set

def profiler(method):
  def profiler_method(*arg, **kw):
    t = perf_counter()
    ret = method(*arg, **kw)
    print(f'{method.__name__} method took : {perf_counter()-t:.4f} sec')
    return ret
  return profiler_method

NEIGHBOURS: List[complex] = [
  complex(-1, -1),
  complex(0, -1),
  complex(1, -1),
  complex(-1, 0),
  complex(1, 0),
  complex(-1, 1),
  complex(0, 1),
  complex(1, 1)
]

# global variables
dirs: List[List[complex]] = [
  [complex(0, -1), complex(-1, -1), complex(1, -1)], # N
  [complex(0, 1), complex(-1, 1), complex(1, 1)],  # S
  [complex(-1, 0), complex(-1, -1), complex(-1, 1)], # W
  [complex(1, 0), complex(1, -1), complex(1, 1)] # E
]

# Part 1: Thanks to @Xodarap for the idea to use 3 sets instead of a large dict
def calc(elves: Set[complex]) -> Tuple[int, int]:
  global checks
  _round: int = 0
  part1_solution: int = 0
  while True: # rounds
    _round += 1
    # first half: propose move
    relations: Dict[complex, complex] = {}
    props: Set[complex] = set()
    dupes: Set[complex] = set()
    for elf in elves:
      if all(elf+n not in elves for n in NEIGHBOURS):
        continue
      prop: complex = None
      for direction in dirs:
        if all(elf + d not in elves for d in direction):
          prop = elf + direction[0]
          break
      if prop == None:
        continue
      if prop in dupes:
        continue
      if prop in props:
        dupes.add(prop)
        continue
      props.add(prop)
      relations[elf] = prop

    # reset all elves that proposed the same move
    relations = {k: v for k, v in relations.items() if v not in dupes}
    neoelves: Set[complex] = set(relations.values())
    remelves: Set[complex] = elves - set(relations.keys())
    elves = neoelves | remelves
    # check if no elf moved
    if len(relations.values()) == 0:
      break

    dirs.append(dirs.pop(0)) # rotate directions list
    
    # save part1 solution
    if _round == 10:
      part1_solution = count_free_fields(elves)
  return part1_solution, _round

def count_free_fields(elves: Set[complex]) -> int:
  # find min max
  r, i = zip(*[(e.real, e.imag) for e in elves])
  x = 1+max(r) - min(r)
  y = 1+max(i) - min(i)
  return x*y-len(elves)

def get_input() -> Set[complex]:
  with open(os.path.dirname(os.path.realpath(__file__))+'/input', 'r', encoding='utf-8') as f:
    content = [[c for c in s.strip()] for s in f.read().rstrip().split('\n')]
  elves: Set[complex] = set()
  for y, l in enumerate(content):
    for x, c in enumerate(l):
      if c == '#':
        elves.add(complex(x, y))
  return elves

@profiler
def solve():
  elves: Set[complex] = get_input()
  print("Part 1: %d\nPart 2: %d" % calc(elves))

if __name__ == "__main__":
  solve()
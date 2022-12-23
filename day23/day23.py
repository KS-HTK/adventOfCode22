# -*- coding: utf-8 -*-

import os
from time import perf_counter
from typing import List, Dict, Tuple, Generator

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
checks: List[List[complex]] = [
  [complex(0, -1), complex(-1, -1), complex(1, -1)], # N
  [complex(0, 1), complex(-1, 1), complex(1, 1)],  # S
  [complex(-1, 0), complex(-1, -1), complex(-1, 1)], # W
  [complex(1, 0), complex(1, -1), complex(1, 1)] # E
]

# Part 1:
def calc(elfs: Dict[complex, List[complex]]) -> Tuple[int, int]:
  global checks
  _round: int = 0
  part1_solution: int = 0
  while True: # rounds
    _round += 1
    moved_count = 0
    # first half: propose move
    neoelfs: Dict[complex, List[complex]] = {}
    for elf in list(elfs):
      moved: bool = False
      if any([f in elfs for f in get_neighbours(elf)]):
        for direction in checks:
          if all([elf + d not in elfs for d in direction]):
            moved = True
            moved_count += 1
            neoelf = elf + direction[0]
            if neoelf in neoelfs:
              neoelfs[neoelf].append(elf)
              break
            else:
              neoelfs[neoelf] = [elf]
              break
      if not moved:
        neoelfs[elf] = [elf]
    # reset all elves that proposed the same move
    for elf in list(neoelfs):
      if len(neoelfs[elf]) > 1:
        for e in neoelfs[elf]:
          moved_count -= 1
          neoelfs[e] = [e]
        del neoelfs[elf]
    # second half: move
    elfs = neoelfs
    checks.append(checks.pop(0)) # rotate directions list
    
    # save part1 solution
    if _round == 10:
      part1_solution = count_free_fields(list(elfs))
    # check if no elf moved
    if moved_count == 0:
      break
  return part1_solution, _round

def get_neighbours(elf: complex) -> Generator[complex, complex, None]:
  for d in NEIGHBOURS:
    yield elf + d

def count_free_fields(elfs: List[complex]) -> int:
  # find min max
  rlist: List[int] = [round(c.real) for c in elfs]
  ilist: List[int] = [round(c.imag) for c in elfs]
  x = 1+max(rlist) - min(rlist)
  y = 1+max(ilist) - min(ilist)
  return x*y-len(elfs)

def get_input() -> Dict[complex, List[complex]]:
  with open(os.path.dirname(os.path.realpath(__file__))+'/input', 'r', encoding='utf-8') as f:
    content = [[c for c in s.strip()] for s in f.read().rstrip().split('\n')]
  elfs = {}
  for y, l in enumerate(content):
    for x, c in enumerate(l):
      if c == '#':
        elfs[complex(x, y)] = []
  return elfs

@profiler
def solve():
  elfs: Dict[complex, List[complex]] = get_input()
  print("Part 1: %d\nPart 2: %d" % calc(elfs))

if __name__ == "__main__":
  solve()
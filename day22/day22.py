# -*- coding: utf-8 -*-

import os
import re
from time import perf_counter
from typing import List, Dict, Tuple, Callable

def profiler(method):
  def profiler_method(*arg, **kw):
    t = perf_counter()
    ret = method(*arg, **kw)
    print(f'{method.__name__} method took : {perf_counter()-t:.4f} sec')
    return ret
  return profiler_method

# Define constants
DIR: Dict[str, complex|Callable[[complex], complex]] = {
  'N': complex(0, -1),
  'E': complex(1, 0),
  'S': complex(0, 1),
  'W': complex(-1, 0),
  'R': lambda c: 1j * c,
  'L': lambda c: 1j**3 * c
}
HEADING: Dict[complex, int] = {
  complex(1, 0): 0,
  complex(0, 1): 1,
  complex(-1, 0): 2,
  complex(0, -1): 3
}

# Define global variables
position: complex = complex(0, 0)
heading: complex = DIR['E'] # start facing east

# Part 1:
def part1(board: Dict[complex, bool], instructions: List[str|int]) -> int:
  global position, heading
  for i in instructions:
    if isinstance(i, int):
      while i > 0:
        loc: complex = position + heading
        if loc not in board:
          while True:
            if loc-heading in board:
              loc -= heading
            else:
              break
        assert(loc in board)
        if board[loc]:
          position = loc
        i-=1
    else:
      heading = DIR[i](heading)
  return int(4*position.real + 1000*int(position.imag) + HEADING[heading])

# Part 2:
def part2(board: Dict[complex, bool], instructions: List[str|int]) -> int:
  global position, heading
  for i in instructions:
    if isinstance(i, int):
      while i > 0:
        loc: complex = position + heading
        head: complex = heading
        if loc not in board:
          # use teleport to find next position and new heading
          loc, head = teleport()
        if loc not in board:
          print(position, heading, loc, head)
        assert(loc in board)
        if board[loc]:
          position = loc
          heading = head
        i-=1
    else:
      heading = DIR[i](heading)
  return int(4*position.real + 1000*int(position.imag) + HEADING[heading])
  
def teleport() -> Tuple[complex, complex]:
  global position, heading
  # normalize position to 1-50
  r: int = (position.real-1)%50+1
  i: int = (position.imag-1)%50+1
  # calculate side of cube
  side: int = ((position.real-1)//50)+2*((position.imag-1)//50)
  h_ind: int = HEADING[heading]
  if side == 1:
    if h_ind == 2:
      # side 1 facing west -> side 4 facing east
      return complex(1, 151-i ), DIR['E']
    elif h_ind == 3:
      # side 1 facing north -> side 6 facing east
      return complex(1, 150+r), DIR['E']
  elif side == 2:
    if h_ind == 0:
      # side 2 facing east -> side 5 facing west
      return complex(100, 151-i), DIR['W']
    elif h_ind == 1:
      # side 2 facing south -> side 3 facing west
      return complex(100, 50+r), DIR['W']
    elif h_ind == 3:
      # side 2 facing north -> side 6 facing north
      return complex(r, 200), DIR['N']
  elif side == 3:
    if h_ind == 0:
      # side 3 facing east -> side 2 facing north
      return complex(100+i, 50), DIR['N']
    elif h_ind == 2:
      # side 3 facing west -> side 4 facing south
      return complex(i, 101), DIR['S']
  elif side == 4:
    if h_ind == 2:
      # side 4 facing west -> side 1 facing east
      return complex(51, 51-i), DIR['E']
    elif h_ind == 3:
      # side 4 facing north -> side 3 facing east
      return complex(51, 50+r), DIR['E']
  elif side == 5:
    if h_ind == 0:
      # side 5 facing east -> side 2 facing west
      return complex(150, 51-i), DIR['W']
    elif h_ind == 1:
      # side 5 facing south -> side 6 facing west
      return complex(50, 150+r), DIR['W']
  elif side == 6:
    if h_ind == 0:
      # side 6 facing east -> side 5 facing north
      return complex(50+i, 150), DIR['N']
    elif h_ind == 1:
      # side 6 facing south -> side 2 facing south
      return complex(100+r, 1), DIR['S']
    elif h_ind == 2:
      # side 6 facing west -> side 1 facing south
      return complex(50+i, 1), DIR['S']

def get_input():
  global position
  with open(os.path.dirname(os.path.realpath(__file__))+'/input', 'r', encoding='utf-8') as f:
    content = [s for s in f.read().rstrip().split('\n')]
  instructions = content.pop()
  content.pop()
  content = [[c for c in s] for s in content]
  # split instructions
  instructions = list(re.split('(\d+)', instructions))
  instructions.pop(0)
  instructions.pop()
  for i, s in enumerate(instructions):
    try:
      instructions[i] = int(s)
    except ValueError:
      pass
  # get initial position
  x = content[0].index('.')
  position = complex(x+1, 1) # set start position
  # parse board
  board = {}
  for y, s in enumerate(content):
    for x, c in enumerate(s):
      if c == '#':
        board[complex(x+1, y+1)] = False
      if c == '.':
        board[complex(x+1, y+1)] = True
  return board, instructions

@profiler
def solve():
  global position, heading
  board, instructions = get_input()
  start_pos = position
  print("Part 1:", part1(board, instructions))
  # reset position and heading
  position = start_pos
  heading = DIR['E']
  print("Part 2:", part2(board, instructions))

if __name__ == "__main__":
  solve()
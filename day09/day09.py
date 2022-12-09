# -*- coding: utf-8 -*-

from typing import List, Dict, Set, Tuple


def solve(cmds: List[List[str]]) -> (int, int):
  directions: Dict[str, Tuple[int, int]] = {
    "U": (0, 1),
    "D": (0, -1),
    "R": (1, 0),
    "L": (-1, 0)
  }
  # the head + 9 tails
  tail: List(Tuple[int, int]) = [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0),
                                 (0, 0), (0, 0), (0, 0), (0, 0), (0, 0)]
  tail1_visited: Set[Tuple[int, int]] = set([tail[1]])
  tail9_visited: Set[Tuple[int, int]] = set([tail[9]])
  for [d, l] in cmds:
    l = int(l)
    while l > 0:
      # Move Head
      tail[0] = add(tail[0], directions[d]) 
      l -= 1
      # Check if tail needs to move
      for i in range(1, len(tail)):
        tail[i] = sim_tail(tail[i-1], tail[i])
      tail1_visited.add(tail[1])
      tail9_visited.add(tail[9])
  return (len(tail1_visited), len(tail9_visited))

def sim_tail(head: Tuple[int, int], tail: Tuple[int, int]) -> Tuple[int, int]:
    moves: Dict[Tuple[int, int], Tuple[int, int]] = move(head)
    if tail in moves.keys():
      # tail needs to move
      return moves[tail]
    return tail

def move(t: Tuple[int, int]) -> Dict[Tuple[int, int], Tuple[int, int]]:
  # this could maybe be done with 
  moves: Dict[Tuple[int, int], Tuple[int, int]] = {
    # in line movements
    add(t, (-2,  0)): add(t, (-1,  0)),
    add(t, ( 0, -2)): add(t, ( 0, -1)),
    add(t, ( 2,  0)): add(t, ( 1,  0)),
    add(t, ( 0,  2)): add(t, ( 0,  1)),
    # diagonal movements
    add(t, (-2, -2)): add(t, (-1, -1)),
    add(t, ( 2,  2)): add(t, ( 1,  1)),
    add(t, (-2,  2)): add(t, (-1,  1)),
    add(t, ( 2, -2)): add(t, ( 1, -1)),
    # knights move
    add(t, (-2, -1)): add(t, (-1,  0)),
    add(t, (-2,  1)): add(t, (-1,  0)),
    add(t, ( 2, -1)): add(t, ( 1,  0)),
    add(t, ( 2,  1)): add(t, ( 1,  0)),
    add(t, (-1, -2)): add(t, ( 0, -1)),
    add(t, ( 1, -2)): add(t, ( 0, -1)),
    add(t, (-1,  2)): add(t, ( 0,  1)),
    add(t, ( 1,  2)): add(t, ( 0,  1)),
  }
  return moves

# tuple addition
def add(t1: Tuple[int, int], t2: Tuple[int, int]) -> Tuple[int, int]:
  return tuple(map(lambda i, j: i + j, t1, t2))

def get_input() -> List[List[str]]:
  with open('day09/input', 'r', encoding='utf-8') as f:
    input = [s.split(" ") for s in f.read().rstrip().split('\n')]
  return input

if __name__ == "__main__":
  input: List[List[str]] = get_input()
  sol: Tuple[int, int] = solve(input)
  print("Part 1:", sol[0])
  print("Part 2:", sol[1])

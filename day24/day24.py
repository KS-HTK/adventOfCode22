# -*- coding: utf-8 -*-

import os
from time import perf_counter
from math import lcm
from typing import List, Tuple, Set, Dict

def profiler(method):
  def profiler_method(*arg, **kw):
    t = perf_counter()
    ret = method(*arg, **kw)
    print(f'{method.__name__} method took : {perf_counter()-t:.4f} sec')
    return ret
  return profiler_method

# Constants N, E, S, W
MOVES: List[Tuple[int, int]] = [(0, 1), (1, 0), (0, -1), (-1, 0),  (0, 0)]
BLIZZARDS: Dict[str, Tuple[int, int]] = {
  '^': (-1, 0),
  '>': (0, 1),
  'v': (1, 0),
  '<': (0, -1)
}

def bfs(valley: List[List[str]], blizzards: List[List[List[int]]], R: int, C: int, T: int,
         source: Tuple[int, int], dest: Tuple[int, int], t_offset: int = 0) -> int:
  dist: List[List[List[int]]] = [[[5000]*T for _ in range(C)] for _ in range(R)]
  queue: List[Tuple[int, int, int]] = list()

  def add(r: int, c: int, t: int, d: int) -> None:
    if r < 0 or c < 0 or r >= R or c >= C or valley[r][c] == '#' or blizzards[r][c][t] > 0:
      return
    if dist[r][c][t] <= d:
      return
    dist[r][c][t] = d
    queue.append((r, c, t))
  
  t_offset = t_offset % T
  add(*source, t_offset, 0)
  while queue:
    r, c, t = queue.pop(0)
    d: int = dist[r][c][t]
    for dr, dc in MOVES:
      add(r+dr, c+dc, (t+1)%T, d+1)

  ret: int = None
  for t in range(T):
    if ret == None:
      ret = dist[dest[0]][dest[1]][t]
    ret = min(ret, dist[dest[0]][dest[1]][t])
  
  return ret

def get_input() -> Tuple[List[List[str]], List[List[List[int]]], int, int, int]:
  with open(os.path.dirname(os.path.realpath(__file__))+'/input', 'r', encoding='utf-8') as f:
    valley = [s.strip() for s in f.read().rstrip().split('\n')]
  lenR = len(valley)
  lenC = len(valley[0])
  T = lcm(lenR-2, lenC-2)
  # generate blizzards map
  blizzards = [[[0]*T for _ in range(lenC)] for _ in range(lenR)]
  
  # adjust position to be within the valley
  def adjust(v, lowV, highV):
    return lowV if v > highV else highV if v < lowV else v

  # for blizzard block position at time
  for row in range(lenR):
    for col in range(lenC):
      if valley[row][col] in BLIZZARDS:
        dr, dc = BLIZZARDS[valley[row][col]]
        r, c = row, col
        for t in range(T):
          blizzards[r][c][t] += 1
          r = adjust(r+dr, 1, lenR-2)
          c = adjust(c+dc, 1, lenC-2)
  return (valley, blizzards, lenR, lenC, T)


@profiler
def solve() -> None:
  _input: Tuple[List[List[str]], List[List[List[int]]], int, int, int] = get_input()
  lenR, lenC = _input[2:-1]
  start: Tuple[int, int] = (0, 1)
  end: Tuple[int, int] = (lenR-1, lenC-2)
  pt1: int = bfs(*_input, start, end, 0)
  ret: int = pt1+bfs(*_input, end, start, pt1)
  pt2: int = ret+bfs(*_input, start, end, ret)
  print("Part 1:", pt1)
  print("Part 2:", pt2)

if __name__ == "__main__":
  solve()
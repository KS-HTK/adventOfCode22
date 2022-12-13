# -*- coding: utf-8 -*-

import os
from time import perf_counter
from typing import List, Tuple

def profiler(method):
    def profiler_method(*arg, **kw):
        t = perf_counter()
        ret = method(*arg, **kw)
        print(f'{method.__name__} method took : {perf_counter()-t:.4f} sec')
        return ret
    return profiler_method

class Packet:
  def __init__(self, packet: Tuple[int|List, int|List]):
    self.packet: Tuple[int|List, int|List] = packet

  def __lt__(self, other) -> bool:
    return in_order(self.packet, other.packet)
  def __gt__(self, other) -> bool:
    return in_order(other.packet, self.packet)
  def __eq__(self, other) -> bool:
    return self.packet == other

# Part 1:
def part1(content) -> int:
  return sum(i for i, p in enumerate(content, 1) if in_order(*p))

# Part 2:
def part2(content) -> int:
  packet2: Packet = Packet([[2]])
  packet6: Packet = Packet([[6]])
  packets: List[Packet] = [packet2, packet6]
  for (p1, p2) in content:
    packets.append(Packet(p1))
    packets.append(Packet(p2))
  packets.sort()
  return (packets.index(packet2)+1)*(packets.index(packet6)+1)

def in_order(left: int|List[int|List], right: int|List[int|List]) -> bool:
  if isinstance(left,int) and isinstance(right,int):
    if left == right:
      return None
    return left < right
  if isinstance(left,int):
    left = [left]
  if isinstance(right,int):
    right = [right]
  for lsub,rsub in zip(left,right):
    sub = in_order(lsub, rsub)
    if sub is not None:
      return sub
  return None if len(left) == len(right) else len(left) < len(right)

def get_input():
  with open(os.path.dirname(os.path.realpath(__file__))+'/input', 'r', encoding='utf-8') as f:
    content = [s.strip() for s in f.read().rstrip().split('\n\n')]
  content = [tuple(map(eval,s.splitlines())) for s in content]
  return content

@profiler
def solve():
  content = get_input()
  print("Part 1:", part1(content))
  print("Part 2:", part2(content))

if __name__ == "__main__":
  solve()
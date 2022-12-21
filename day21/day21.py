# -*- coding: utf-8 -*-

import os
from time import perf_counter
from sympy import simplify, solveset, symbols
from typing import List, Dict, Tuple, Callable

def profiler(method):
  def profiler_method(*arg, **kw):
    t = perf_counter()
    ret = method(*arg, **kw)
    print(f'{method.__name__} method took : {perf_counter()-t:.4f} sec')
    return ret
  return profiler_method

# Part 1:
def part1(content: Dict[str, int|Tuple[str, str, Callable[[int, int], int]]]) -> int:
  while not isinstance(content['root'], int):
    for k, v in content.items():
      if isinstance(v, int):
        continue
      if isinstance(content[v[0]], int) and isinstance(content[v[1]], int):
        content[k] = round(v[2](content[v[0]], content[v[1]]))
  return content['root']

# Part 2: (original implementation)
def original_part2(content: List[complex|Tuple[str, str, Callable[[complex, complex], complex]]]) -> str:
  content['humn'] = 1j
  while not isinstance(content['root'], complex):
    for k, v in content.items():
      if isinstance(v, complex):
        continue
      if (isinstance(content[v[0]], complex) and isinstance(content[v[1]], complex)):
        if k == 'root':
          res = content[v[1]] - content[v[0]]
          res = res.real / float(res.imag)
          return abs(int(res))
        content[k] = v[2](content[v[0]], content[v[1]])

# Improved Part 2: (using sympy) I did this because my original implementation seems like a hack.
# It would fail if any part where humn is used would get squared.
def part2(content: List[int|Tuple[str, str, str]]) -> int:
  nodes: Dict[str, Node] = {}
  for k, v in content.items():
    if k == 'humn':
      nodes[k] = Node(symbols('humn'))
    elif isinstance(v, int):
      nodes[k] = Node(v)
    else:
      nodes[k] = Node(None, v[0], v[1], v[2])
  for k in nodes.keys():
    if nodes[k].val is None:
      nodes[k].left = nodes[nodes[k].left]
      nodes[k].right = nodes[nodes[k].right]
  root = nodes['root']
  return solveset(simplify(root.left.__repr__()) - simplify(root.right.__repr__())).args[0]

class Node:
  def __init__(self, val, left=None, right=None, oppstr=None):
    self.val = val
    self.left = left
    self.right = right
    self.oppstr = oppstr

  def __repr__(self):
    if self.val is not None:
      return self.val.__repr__()
    return f'({self.left.__repr__()} {self.oppstr} {self.right.__repr__()})'


OPPMAP = {
  '+': lambda a, b: a+b,
  '-': lambda a, b: a-b,
  '*': lambda a, b: a*b,
  '/': lambda a, b: a/b,
}

def get_input():
  with open(os.path.dirname(os.path.realpath(__file__))+'/input', 'r', encoding='utf-8') as f:
    content = [s.strip() for s in f.read().rstrip().split('\n')]
  m1, m2, m3 = {}, {}, {}
  for l in content:
    k, v = l.split(': ')
    try:
      v = int(v)
    except ValueError:
      pass
    else:
      m1[k] = v
      m2[k] = complex(v, 0)
      m3[k] = v
      continue
    v = v.split(' ')
    m1[k] = (v[0], v[2], OPPMAP[v[1]])
    m2[k] = (v[0], v[2], OPPMAP[v[1]])
    m3[k] = (v[0], v[2], v[1])
  return m1, m2, m3

@profiler
def solve():
  m1, m2, m3 = get_input()
  print("Part 1:", part1(m1))
  print("Part 2:", original_part2(m2))
  #print("Part 2:", part2(m3))
  

if __name__ == "__main__":
  solve()
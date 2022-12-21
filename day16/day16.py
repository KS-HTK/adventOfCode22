# -*- coding: utf-8 -*-

import os
import re
from time import perf_counter
from typing import Dict, Set

def profiler(method):
  def profiler_method(*arg, **kw):
    t = perf_counter()
    ret = method(*arg, **kw)
    print(f'{method.__name__} method took : {perf_counter()-t:.4f} sec')
    return ret
  return profiler_method

# Part 1:
def part1(valves: Dict[str, Dict]) -> int:
  best = 0
  def search(opened, flowed, pos, time_rem):
    nonlocal best
    if flowed > best:
      best = flowed
    if time_rem <= 0:
      return
    if pos not in opened:
      search(opened.union([pos]), flowed + valves[pos]['flow']*time_rem, pos, time_rem-1)
    else:
      for k in [x for x in valves[pos]['paths'].keys() if x not in opened]:
        search(opened, flowed, k, time_rem - valves[pos]['paths'][k])

  search(set(['AA']), 0, 'AA', 29)
  return best

# Part 2:
def part2(valves: Dict[str, Dict]) -> int:
  best: int = 0
  def search(opened: Set[str], flowed: int, pos: str, time_rem: int, elephants_turn: bool):
    nonlocal best
    if flowed > best:
      best = flowed
    if time_rem <= 0:
      return
    if pos not in opened:
      search(opened.union([pos]), flowed + valves[pos]['flow']*time_rem, pos, time_rem-1, elephants_turn)
      if not elephants_turn:
        search(set([pos]).union(opened), flowed + valves[pos]['flow']*time_rem, 'AA', 25, True)
    else:
      for k in [x for x in valves[pos]['paths'].keys() if x not in opened]:
        search(opened, flowed, k, time_rem - valves[pos]['paths'][k], elephants_turn)
  
  search(set(['AA']), 0, 'AA', 25, False)
  return best

# Aternative to part 1 & 2:
# Way faster than part 2, but not as fast as part 1
# Idea curtesy of Xodarap
def calc(valves: Dict[str, Dict], time: int = 30) -> int:
  pathset = set()
  def generate_paths(pos, path, time_rem):
    for k in [x for x in valves[pos]['paths'].keys() if x not in path]:
      required_time = valves[pos]['paths'][k]+1 # go to destination + open valve
      if time_rem - required_time <= 0:
        continue
      pathset.add(tuple(path+[k]))
      generate_paths(k, path + [k], time_rem - required_time)
  generate_paths('AA', ['AA'], time)

  def e_paths(humanpath):
    e_pathset = set()
    def elephant_paths(pos, path, time_rem, humanpath):
      for k in [x for x in valves[pos]['paths'].keys() if x not in path and x not in humanpath]:
        required_time = valves[pos]['paths'][k]+1 # go to destination + open valve
        if time_rem - required_time <= 0:
          continue
        e_pathset.add(tuple(path+[k]))
        elephant_paths(k, path + [k], time_rem - required_time, humanpath)
    elephant_paths('AA', ['AA'], time, humanpath)
    return e_pathset
  
  def get_flow(path):
    flow = 0
    _time = time
    for i in range(len(path)-1):
      _time -= valves[path[i]]['paths'][path[i+1]] # go to destination
      _time -= 1 # open valve
      flow += valves[path[i+1]]['flow']*_time
      if _time <= 0:
        print("Time ran out")
        return -1
    return flow
  
  optimum = max(get_flow(x) for x in pathset)
  if time == 30:
    return optimum

  # Part 2:
  max_flow = 0
  for path in pathset:
    h_flow = get_flow(path)
    if h_flow < max_flow - optimum:
      continue
    e_flow = max(get_flow(x) for x in e_paths(path))
    if h_flow + e_flow > max_flow:
      max_flow = h_flow + e_flow
  return max_flow

def bfs(valves: Dict[str, Dict], front: Set[str], end: str) -> int:
  depth: int = 1
  while True:
    next_front: Set[str] = set()
    for x in front:
      if x == end:
        return depth
      for y in valves[x]['tunnels']:
        next_front.add(y)
    front = next_front
    depth += 1

def get_input():
  with open(os.path.dirname(os.path.realpath(__file__))+'/input', 'r', encoding='utf-8') as f:
    content = [s.strip() for s in f.read().rstrip().split('\n')]
  letters = re.compile(r'[A-Z]{2}')
  valves = {}
  for l in content:
    valve = letters.findall(l)[0]
    tunnels = letters.findall(l)[1:]
    flow = int(l.split(';')[0].split('=')[1])
    valves[valve] = {'flow': flow, 'tunnels': tunnels, 'paths': {}}
  return valves

@profiler
def solve():
  valves = get_input()
  keys = sorted([x for x in list(valves.keys()) if valves[x]['flow'] != 0])
  for k in keys + ['AA']:
    for k2 in keys:
      if k2 != k:
        valves[k]['paths'][k2] = bfs(valves, valves[k]['tunnels'], k2)
  print("Part 1:", part1(valves))
  print("Part 2:", calc(valves, 26))

if __name__ == "__main__":
  solve()
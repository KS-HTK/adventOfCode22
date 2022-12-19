# -*- coding: utf-8 -*-

import os
import re
from time import perf_counter
from typing import List, Dict, Tuple

def profiler(method):
  def profiler_method(*arg, **kw):
    t = perf_counter()
    ret = method(*arg, **kw)
    print(f'{method.__name__} method took : {perf_counter()-t:.4f} sec')
    return ret
  return profiler_method

# Part 1:
def part1(bps: Dict[int, List[Tuple[int, int, int, int]]]) -> int:
  quality_sum: int = 0
  for bp_id, robot_costs in bps.items():
    num_mined: int = bfs(robot_costs, (1,0,0,0), 24)
    quality_sum += num_mined*bp_id
  return quality_sum

# Part 2:
def part2(bps: Dict[int, List[Tuple[int, int, int, int]]]) -> int:
  mined: int = 1
  for bp_id, robot_costs in bps.items():
    # truncate blueprints
    if bp_id > 3:
      break
    num_mined: int = bfs(robot_costs, (1, 0, 0, 0), 32)
    mined *= num_mined
  return mined

# the max_queue value should be increased to 5000 if you are unsure about the results
def bfs(costs, robots, num_time, max_queue = 125) -> int:
  def quality(state) -> int:
    _, (_, _, mined) = state
    return 1000*mined[3] + 100*mined[2] + 10*mined[1] + mined[0]
  
  queue = list()
  queue.append((0, (robots, (0,0,0,0), (0,0,0,0)))) 
  max_geodes: int = 0
  depth: int = 0
  while queue:
    time, (robots, resources, mined) = queue.pop(0)
    # Prune search space
    if time > depth: 
      queue.sort(key=quality, reverse=True)
      queue = queue[:max_queue]
      depth = time

    if time == num_time:
      max_geodes = max(max_geodes, mined[3])
      continue
      
    # Mine resources
    new_resources = tuple([resources[i] + robots[i] for i in range(4)])
    new_mined = tuple([mined[i] + robots[i] for i in range(4)])

    # Don't build robot
    queue.append((time+1, (robots, new_resources, new_mined)))
    # Build robots
    for i in range(4):
      cost_robot = costs[i]
      if all([resources[j] >= cost_robot[j] for j in range(4)]):
        new_robots = list(robots)
        new_robots[i] += 1
        new_robots = tuple(new_robots)

        new_state = tuple([new_resources[i] - cost_robot[i] for i in range(4)])
        queue.append((time+1, (new_robots, new_state, new_mined)))
  return max_geodes

def get_input():
  with open(os.path.dirname(os.path.realpath(__file__))+'/input', 'r', encoding='utf-8') as f:
    costs = [[int(i) for i in re.findall(r'\d+' ,s)] for s in f.read().rstrip().splitlines()]
  blueprints: Dict[int, List[Tuple[int, int, int, int]]] = dict()
  for _bp_id, _o, _c, _o1, _o2, _g1, _g2 in costs:
    blueprints[_bp_id] = [
      (_o, 0, 0, 0),
      (_c, 0, 0, 0),
      (_o1, _o2, 0, 0),
      (_g1, 0, _g2, 0)
    ]
  return blueprints

@profiler
def solve():
  bps: Dict[int, List[Tuple[int, int, int, int]]] = get_input()
  print("Part 1:", part1(bps))
  print("Part 2:", part2(bps))

if __name__ == "__main__":
  solve()
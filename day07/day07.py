# -*- coding: utf-8 -*-

from typing import List, Dict
from collections import deque
from time import perf_counter

def profiler(method):
  def profiler_method(*arg, **kw):
    t = perf_counter()
    ret = method(*arg, **kw)
    print(f'{method.__name__} method took : {perf_counter()-t:.4f} sec')
    return ret
  return profiler_method

class Dir:
  def __init__(self):
    self.content = []

  def get_size(self):
    return sum([c.get_size() for c in self.content])

  def append(self, content):
    self.content.append(content)

class File:
  def __init__(self, size):
    self.size = size

  def get_size(self):
    return self.size

# Part 1:
def part1(dirs: Dict[str, Dir]) -> int:
  return sum([obj.get_size() if obj.get_size() < 100000 else 0 for obj in dirs.values()])

# Part 2:
def part2(dirs: Dict[str, Dir]) -> int:
  used = dirs["/"].get_size()
  freeup = 30000000-(70000000-used)
  best = used
  for obj in dirs.values():
    if obj.get_size()>=freeup and obj.get_size() < best:
      best = obj.get_size()
  return best

def get_tree(input: List[str]):
  input = deque(input)
  dirs = {}
  path = ""
  while len(input) != 0:
    line = input.popleft()
    if line == "$ cd /":
      path = "/"
      if path not in dirs:
        dirs[path] = Dir()
      continue
    elif line == "$ ls" and len(input) >= 1:
      line = input.popleft()
      dir_obj = dirs[path]
      while True:
        line = line.split()
        tmp_path = path + "/" if path != "/" else path
        if line[0] == "dir":
          tmp_path += line[1]
          if tmp_path not in dirs:
            dirs[tmp_path] = Dir()
          dir_obj.append(dirs[tmp_path])
        else:
          tmp_path += line[1]
          file_obj = File(int(line[0]))
          dir_obj.append(file_obj)
        if len(input) != 0 and not input[0].startswith("$"):
          line = input.popleft()
        else:
          break
    elif line == "$ cd ..":
      if path == "/":
        continue
      else:
        path = path.split("/")
        path = "/".join(path[:-1])
    elif line.startswith("$ cd"):
      line = line.split()
      if path == "/":
        path += line[2]
      else:
        path += "/" + line[2]
      if path not in dirs:
        dirs[path] = Dir()
  return dirs

def get_input():
  with open('day07/input', 'r', encoding='utf-8') as f:
    input = [s.strip() for s in f.read().rstrip().split('\n')]
  return input

@profiler
def solve():
  input = get_input()
  tree = get_tree(input)
  print("Part 1:", part1(tree))
  print("Part 2:", part2(tree))

if __name__ == "__main__":
  solve()

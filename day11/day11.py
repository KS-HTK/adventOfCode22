# -*- coding: utf-8 -*-

import os
import re
from time import perf_counter
from typing import List, Callable

def profiler(method):
  def profiler_method(*arg, **kw):
      t = perf_counter()
      ret = method(*arg, **kw)
      print(f'{method.__name__} method took : {perf_counter()-t:.4f} sec')
      return ret
  return profiler_method

class Monkey():
  def __init__(self, monkey_str: List[str]) -> None:
    nums: Callable[[str], List[int]] = lambda s: map(int, re.findall(r'\d+', s))
    sint: Callable[[str], int] = lambda s: int(re.search(r'\d+', s).group())
    self.id: int = sint(monkey_str[0])
    self.items: List[int] = list(nums(monkey_str[1]))
    self.operation_str: str = monkey_str[2].split(' = ')[1].replace('old', 'x')
    self.operation: Callable[[int], int] = self.parse_Op()
    self.testVal: int = sint(monkey_str[3])
    self.test: Callable[[int], bool] = lambda x: x % self.testVal == 0
    self.trueID: int = sint(monkey_str[4])
    self.falseID: int = sint(monkey_str[5])
    self.true: Monkey = None
    self.false: Monkey = None
    self.divisor: int = None
    self.activity: int = 0

  def parse_Op(self) -> Callable[[int], int]:
    op = self.operation_str.split(' ')
    if op[1] == '+':
      if op[2] == 'x':
        return lambda x: x + x
      else:
        return lambda x: x + int(op[2])
    elif op[1] == '*':
      if op[2] == 'x':
        return lambda x: x * x
      else:
        return lambda x: x * int(op[2])
    else:
      # function could be:
      return lambda x: eval(self.operation_str)
      # but this is very slow in execution, so only used if not manualy parsed

  def next_item(self, pt2: bool) -> int:
    item = self.operation(self.items.pop(0))
    if not pt2:
      item = item//3
    self.activity += 1
    if self.test(item):
      self.true.items.append(item%self.divisor if pt2 else item)
    else:
      self.false.items.append(item%self.divisor if pt2 else item)

  def do_round(self, pt2: bool = False) -> None:
    while len(self.items) > 0:
      self.next_item(pt2)


# Part 1:
def part1(monkey_list: List[Monkey]) -> int:
  for _ in range(20):
    for m in monkey_list:
      m.do_round()

  monkey_list.sort(key=lambda m: m.activity)
  return monkey_list[-1].activity * monkey_list[-2].activity

# Part 2:
def part2(monkey_list: List[Monkey]) -> int:
  for _ in range(10000):
    for m in monkey_list:
      m.do_round(pt2 = True)

  monkey_list.sort(key=lambda m: m.activity)
  return monkey_list[-1].activity * monkey_list[-2].activity

def get_input() -> List[str]:
  with open(os.path.dirname(os.path.realpath(__file__))+'/input', 'r', encoding='utf-8') as f:
    content = [s.split('\n') for s in f.read().rstrip().split('\n\n')]
  return content

@profiler
def solve():
  content: List[str] = get_input()
  monkeys1: List[Monkey] = [None]*len(content)
  monkeys2: List[Monkey] = [None]*len(content)
  divisor: int = 1
  for part in content:
    m1 = Monkey(part)
    m2 = Monkey(part)
    divisor *= m2.testVal
    monkeys1[m1.id] = m1
    monkeys2[m2.id] = m2
  for m_l in [monkeys1, monkeys2]:
    for m in m_l:
      m.divisor = divisor
      m.true = m_l[m.trueID]
      m.false = m_l[m.falseID]

  print("Part 1:", part1(monkeys1))
  print("Part 2:", part2(monkeys2))

if __name__ == "__main__":
  solve()
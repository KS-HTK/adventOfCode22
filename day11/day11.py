# -*- coding: utf-8 -*-

import os
import re
from typing import List

class Monkey():
  def __init__(self, monkey_str: List[str]):
    nums = lambda s: map(int, re.findall(r'\d+', s))
    sint = lambda s: int(re.search(r'\d+', s).group())
    self.id = sint(monkey_str[0])
    self.items = list(nums(monkey_str[1]))
    self.operation = monkey_str[2]
    self.testVal = sint(monkey_str[3])
    self.test = lambda x: x % self.testVal == 0
    self.trueID = sint(monkey_str[4])
    self.falseID = sint(monkey_str[5])
    self.true = None
    self.false = None
    self.activity = 0
    self.parse_Op()

  def set_true(self, m) -> None:
    self.true = m
  def set_false(self, m) -> None:
    self.false = m
  
  def give(self, item: int) -> None:
    self.items.append(item)

  def parse_Op(self) -> None:
    op = self.operation.split(' = ')[1].split(' ')
    if op[1] == '+':
      if op[2] == 'old':
        self.operation = lambda x: x + x
      else:
        self.operation = lambda x: x + int(op[2])
    elif op[1] == '*':
      if op[2] == 'old':
        self.operation = lambda x: x * x
      else:
        self.operation = lambda x: x * int(op[2])

  def next_item(self, pt2, divisor) -> int:
    item = self.operation(self.items.pop(0))
    if not pt2:
      item = item//3
    self.activity += 1
    if self.test(item):
      self.true.give(item%divisor if pt2 else item)
    else:
      self.false.give(item%divisor if pt2 else item)

  def do_round(self, pt2 = False, divisor = 1) -> None:
    while len(self.items) > 0:
      self.next_item(pt2, divisor)
    assert len(self.items) == 0
    

# Part 1:
def part1(monkey_list: List[object]) -> int:
  for i in range(20):
    for m in monkey_list:
      m.do_round()

  monkey_list.sort(key=lambda m: m.activity)
  return monkey_list[-1].activity * monkey_list[-2].activity

# Part 2:
def part2(monkey_list: List[object]) -> int:
  divisor: int = 1
  for m in monkey_list:
    divisor *= m.testVal

  for _ in range(10000):
    for m in monkey_list:
      m.do_round(pt2 = True, divisor=divisor)

  monkey_list.sort(key=lambda m : m.activity)
  return monkey_list[-1].activity * monkey_list[-2].activity

def get_input():
  with open(os.path.dirname(os.path.realpath(__file__))+'/input', 'r', encoding='utf-8') as f:
    input = [s.split('\n') for s in f.read().rstrip().split('\n\n')]
  return input

if __name__ == "__main__":
  input = get_input()
  monkeys = list(input)
  monkeys2 = list(input)
  for monkey in input:
    m = Monkey(monkey)
    m2 = Monkey(monkey)
    i = m.id
    monkeys[i] = m
    monkeys2[i] = m2
  for m in monkeys:
    m.set_true(monkeys[m.trueID])
    m.set_false(monkeys[m.falseID])
  for m in monkeys2:
    m.set_true(monkeys2[m.trueID])
    m.set_false(monkeys2[m.falseID])

  print("Part 1:", part1(monkeys))
  print("Part 2:", part2(monkeys2))
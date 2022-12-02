# -*- coding: utf-8 -*-

from typing import List

# 1 = Rock
# 2 = Paper
# 3 = Scisors
lookup = {
  'A': 1,
  'B': 2,
  'C': 3,
  'X': 1,
  'Y': 2,
  'Z': 3,
}

input: List[str] = None
with open('day02/input', 'r', encoding='utf-8') as f:
  input = f.read()
  input = input.rstrip().split('\n')
  input = list(map(lambda s: s.split(' '), input))

# Part 1:
def part1(round: List[List[str]]=None):
  my_score: int = 0
  for [op, me] in round:
    my_score += get_round_score(lookup[me], lookup[op])
    

  return my_score


# Part 2:
def part2(round: List[List[str]]=None):
  my_score: int = 0
  for [op, outcome] in round:
    op = lookup[op]
    me = op if outcome=='Y' else ((op+2) if outcome=='X' else (op+1))
    me = me if me<=3 else me-3
    my_score += get_round_score(me, op)

  return my_score


def get_round_score(me:int, op:int)->int:
    if (op==me):
      # Draw
      return me+3
    if (me==op+1 or me==1 and op==3):
      # me Win
      return me+6
    else:
      # me Lose
      return me


if __name__ == "__main__":
  print("Part 1:", part1(input))
  print("Part 2:", part2(list(input)))
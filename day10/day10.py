# -*- coding: utf-8 -*-

from typing import List

# Part 1:
def part1(lines: List[str]) -> int:
  signals: List[int] = []
  nextLook = 20
  clock = 0
  regX = 1
  for line in lines:
    clock+=1
    if clock == nextLook:
      nextLook+=40
      signals.append(regX*clock)
    if line == "noop":
      continue
    clock+=1
    if clock == nextLook:
      nextLook+=40
      signals.append(regX*clock)
    [_, val] = line.split(" ")
    regX += int(val)
  print(signals, clock, nextLook)
  return sum(signals)

# Part 2:
def part2(lines: List[str]) -> str:
  screen: str = ''
  clock = 0
  regX = 1
  for line in lines:
    if clock%40 in [regX-1, regX, regX+1]:
      screen+="#"
    else:
      screen+=" "
    clock+=1
    if line == "noop":
      continue
    if clock%40 in [regX-1, regX, regX+1]:
      screen+="#"
    else:
      screen+=" "
    clock+=1
    [_, val] = line.split(" ")
    regX += int(val)
  return '\n'.join([screen[i:i+40] for i in range(0, len(screen), 40)])

def get_input():
  with open('day10/input', 'r', encoding='utf-8') as f:
    input = [s.strip() for s in f.read().rstrip().split('\n')]
  return input

if __name__ == "__main__":
  input = get_input()
  print("Part 1:", part1(input))
  print("Part 2:")
  print(part2(input))
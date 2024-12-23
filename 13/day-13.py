import numpy as np

def process_line(line, ch):
  line.strip()
  val_str = line.split(":")[1]
  val_strs = val_str.split(",")
  x = int(val_strs[0].split(ch)[1])
  y = int(val_strs[1].split(ch)[1])
  return x, y

# Slightly round number due to floating point imprecision
def is_almost_integer(num):
  return abs(num - round(num)) < 1e-3

def main():
  # Read input
  mach_params = []
  new_mach_params = []

  with open("input.txt", "r") as file:
      line = file.readline()  # Button A
      while line:
          ax, ay = process_line(line, "+")
          line = file.readline()  # Button B
          bx, by = process_line(line, "+")
          line = file.readline()  # Prize
          X, Y = process_line(line, "=")
          line = file.readline()  # Newline Seperation
          line = file.readline()  # Button A
          ab = np.array([[ax, bx], [ay, by]])
          P = np.array([X, Y])
          new_P = np.array([10000000000000 + X, 10000000000000 + Y])
          mach_params.append((ab, P))
          new_mach_params.append((ab, new_P))

  # Part 1
  cost = 0
  for mach in mach_params:
    ab = mach[0]
    P = mach[1]

    moves = np.linalg.solve(ab, P)
    if is_almost_integer(moves[0]) and is_almost_integer(moves[1]):
      cost += 3 * moves[0] + moves[1]

  print(round(cost))

  # Part 2
  new_cost = 0
  for mach in new_mach_params:
    ab = mach[0]
    P = mach[1]

    moves = np.linalg.solve(ab, P)
    if is_almost_integer(moves[0]) and is_almost_integer(moves[1]):
      new_cost += 3 * moves[0] + moves[1]

  print(round(new_cost))

main()
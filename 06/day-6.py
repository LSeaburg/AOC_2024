directions = [
  [0,1], [1,0], [0,-1], [-1,0]
]

def get_guard_pos(map):
  for index, line in enumerate(map):
    if "^" in line:
      return [index, line.index("^")]
    
def next_guard_pos(pos, direction):
  return [pos[0] + direction[0], pos[1] + direction[1]]

def is_in_bounds(pos, map):
  if pos[0] < 0:
    return False
  if pos[1] < 0:
    return False
  if pos[0] > len(map) - 1:
    return False
  if pos[1] > len(map[0]) - 1:
    return False
  return True

def is_barrier(pos, map):
  if map[pos[0]][pos[1]] == "#":
    return True
  return False

def turn(direction, directions):
  for i, dir in enumerate(directions):
    if direction == dir:
      if i == len(directions) - 1:
        return directions[0]
      return directions[i + 1]
  return -1

def count_walked_squares(map):
  sum = 0
  for line in map:
    sum = sum + line.count("X")
  return sum

# Keeps a list of turns that the guard has made
# If the guard makes the same turn in the same position, the
#   guard must be in a loop
def path_loops(state, map):
  seen = []
  pos = state[0]
  direction = state[1]
  while is_in_bounds(next_guard_pos(pos, direction), map):
    if is_barrier(next_guard_pos(pos, direction), map):
      seen.append(state)
      direction = turn(direction, directions)
    else:
      pos = next_guard_pos(pos, direction)
    state = [pos, direction]
    if state in seen:
      return True
  return False

def main():
  # Read input
  f = open("input.txt")
  lines = f.readlines()

  map = []
  for line in lines:
    map.append(list(line.strip()))

  # Part 1
  pos = get_guard_pos(map)
  direction = directions[3]
  initial_guard_state = [pos, direction]

  # Moves the guard until he is out-of-bounds, marking each square with an X
  while is_in_bounds(next_guard_pos(pos, direction), map):
    if is_barrier(next_guard_pos(pos, direction), map):
      direction = turn(direction, directions)
    else:
      map[pos[0]][pos[1]] = "X"
      pos = next_guard_pos(pos, direction)

  map[pos[0]][pos[1]] = "X"
  print(count_walked_squares(map))

  # Part 2
  pos = initial_guard_state[0]

  map[pos[0]][pos[1]] = "^"

  locations = 0

  # Places a new barrier at a visited position, 
  #   resets the guard position and test for a loop
  for i in range(len(map)):
    for j in range(len(map[0])):
      if map[i][j] == "X":
        map[i][j] = "#"
        if path_loops(initial_guard_state, map):
          locations += 1
        map[i][j] = "X"

  print(locations)

main()
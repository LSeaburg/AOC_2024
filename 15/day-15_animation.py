import time

def wide_input(line):
  new_line = []
  for ch in line:
    if ch == "#":
      new_line.append("#")
      new_line.append("#")
    elif ch == "O":
      new_line.append("[")
      new_line.append("]")
    elif ch == ".":
      new_line.append(".")
      new_line.append(".")
    elif ch == "@":
      new_line.append("@")
      new_line.append(".")
  return new_line

def get_move_vec(move):
  if move == "^":
    return (0, 1)
  if move == "v":
    return (0, -1)
  if move == "<":
    return (-1, 0)
  if move == ">":
    return (1, 0)
  return (0,0)

def new_pos(pos, dir):
  vec = get_move_vec(dir)
  return (pos[0] + vec[0], pos[1] - vec[1])

def is_vertical_move(dir):
  if dir == "^" or dir == "v":
    return True
  
def set_map(pos, sym, map):
  (x, y) = pos
  map[y][x] = sym
  return

def get_sym(pos, map):
  (x, y) = pos
  return map[y][x]

def get_robot_pos(map):
  for y, row in enumerate(map):
    if "@" in row:
      return (row.index("@"), y)
    
def is_wall(pos, map):
  (x, y) = pos
  if map[y][x] == "#":
    return True
  return False

def is_box(pos, map):
  (x, y) = pos
  if map[y][x] == "O" or map[y][x] == "[" or map[y][x] == "]":
    return True
  return False

def is_left_edge_of_box(pos, map):
  (x, y) = pos
  if map[y][x] == "[":
    return True
  return False

def is_right_edge_of_box(pos, map):
  (x, y) = pos
  if map[y][x] == "]":
    return True
  return False

def move_box(pos, dir, map, move_half=True, update=True):
  # Move the other half of the box, if necessary
  if is_vertical_move(dir) and move_half:  
    if is_left_edge_of_box(pos, map):
      if not move_box(new_pos(pos, ">"), dir, map, move_half=False, update=update):
        return False
    elif is_right_edge_of_box(pos, map):
      if not move_box(new_pos(pos, "<"), dir, map, move_half=False, update=update):
        return False

  # Cannot update if there is a wall
  if is_wall(new_pos(pos, dir), map):
    return False

  # If there is a box in the space that this box is being moved to, move it
  if is_box(new_pos(pos, dir), map):
    if not move_box(new_pos(pos, dir), dir, map, update=update):
      return False

  # Move the box
  if update:
    set_map(new_pos(pos, dir), get_sym(pos, map), map)
    set_map(pos, ".", map)
  return True

def process_move(dir, map):
  pos = get_robot_pos(map)

  # Need to ask first without updating in case of branching possibilities with wide boxes
  if move_box(pos, dir, map, update=False):
    move_box(pos, dir, map)
    set_map(new_pos(pos, dir), "@", map)
    set_map(pos, ".", map)
  return

def display_map(map):
  CURSOR_UP = "\033[F"

  for row in map:
    for ch in row:
      print(ch, end="")
    print()

  print(CURSOR_UP * (len(map)), end="")
  time.sleep(0.01)
  return

def main():

  map = []
  moves = ""

  with open("input.txt", "r") as file:
    line = file.readline().strip()
    while line:
        map.append(list(line))
        line = file.readline().strip()
    line = file.readline().strip()
    while line:
        moves += line
        line = file.readline().strip()

  for move in moves:
    process_move(move, map)

  gps_sum = 0
  for y, row in enumerate(map):
    for x, ch in enumerate(row):
      if is_box((x, y), map):
        gps_sum += 100 * y + x

  # print(gps_sum)

  map = []
  moves = ""

  with open("input.txt", "r") as file:
      line = file.readline().strip()
      while line:
          map.append(wide_input(line))
          line = file.readline().strip()
      line = file.readline().strip()
      while line:
          moves += line
          line = file.readline().strip()

  # display_map(map)

  for move in moves:
    process_move(move, map)

    # print()
    # print(move)
    display_map(map)

  gps_sum = 0
  for y, row in enumerate(map):
    for x, _ in enumerate(row):
      if is_left_edge_of_box((x, y), map):
        gps_sum += 100 * y + x

  # print(gps_sum)



main()
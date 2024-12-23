from collections import namedtuple

Position = namedtuple("Posiion", ("x", "y"))

def display(race_map):
  for y, row in enumerate(race_map):
    for x, sym in enumerate(row):
      print(f"{sym:<5}", end="")
    print()

def is_in_bounds(pos, race_map):
  if pos.x < 0 or pos.y < 0:
    return False
  if pos.x > len(race_map[0]) - 1:
    return False
  if pos.y > len(race_map) - 1:
    return False
  return True

def is_on_path(pos, race_map):
  if is_in_bounds(pos, race_map) and race_map[pos.y][pos.x] != "#":
    return True
  return False

# Finds (only) unvisited neighbor that is on the path
def get_next_pos(cur, race_map):
  syms = [".", "E"]
  if race_map[cur.y+1][cur.x] in syms:
    return Position(cur.x, cur.y + 1), race_map[cur.y+1][cur.x]
  if race_map[cur.y-1][cur.x] in syms:
    return Position(cur.x, cur.y - 1), race_map[cur.y-1][cur.x]
  if race_map[cur.y][cur.x+1] in syms:
    return Position(cur.x + 1, cur.y), race_map[cur.y][cur.x+1]
  if race_map[cur.y][cur.x-1] in syms:
    return Position(cur.x - 1, cur.y), race_map[cur.y][cur.x-1]
  Exception("no valid neighbors")

# Changes every area on the map track to an int representing 
#   that position in the track
def enumerate_track(start, race_map):
  sym = "."
  cur = start
  num = 0

  while sym != "E":
    race_map[cur.y][cur.x] = num
    num = num + 1
    cur, sym = get_next_pos(cur, race_map)

  race_map[cur.y][cur.x] = num
  return

# Creates 'diamond-shape' around position
def get_cheats(cur, CHEAT_LENGTH, race_map):
  locs = set()
  for length in range(2, CHEAT_LENGTH + 1):
    for x in range(length+1):
      y = length - x
      pos_locs = set()
      pos_locs.add(Position(cur.x + x, cur.y + y))
      pos_locs.add(Position(cur.x - x, cur.y + y))
      pos_locs.add(Position(cur.x + x, cur.y - y))
      pos_locs.add(Position(cur.x - x, cur.y - y))
      for pos in pos_locs:
        if is_on_path(pos, race_map):
          locs.add((pos, length))
  return locs

# Generates list of possible cheats and counts number within threshold
def count_cheats(race_map, CHEAT_LENGTH, CHEAT_THRESHOLD):
  cheats = 0
  for y in range(1, len(race_map) - 1):
    for x in range(1, len(race_map[0]) - 1):
      cur = Position(x, y)
      if is_on_path(cur, race_map):
        for pos, length in get_cheats(cur, CHEAT_LENGTH, race_map):
          if race_map[pos.y][pos.x] - race_map[cur.y][cur.x] - length >= CHEAT_THRESHOLD:
            cheats += 1
  return cheats
  
def main():
  # Read input 
  CHEAT_THRESHOLD = 100
  race_map = []

  with open("input.txt", "r") as file:
    line = file.readline().strip()
    while line:
      race_map.append(list(line))
      line = file.readline().strip()

  # Change map path to int for position in maze
  for y, row in enumerate(race_map):
    for x, sym in enumerate(row):
      if sym == "S":
        start = Position(x, y)

  enumerate_track(start, race_map)

  # Part 1
  cheats = count_cheats(race_map, 2, CHEAT_THRESHOLD)
  print(cheats)

  # Part 2
  cheats = count_cheats(race_map, 20, CHEAT_THRESHOLD)
  print(cheats)

main()
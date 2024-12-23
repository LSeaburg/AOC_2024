import itertools

def is_in_bounds(pos, map):
  if pos[0] < 0 or pos[1] < 0:
    return False
  if pos[0] >= len(map[0]):
    return False
  if pos[1] >= len(map):
    return False
  return True

# Travel in vector away from each antinode
def get_antinodes(ant_locs):
  vector = (ant_locs[1][0] - ant_locs[0][0], ant_locs[1][1] - ant_locs[0][1])
  an1 = (ant_locs[0][0] - vector[0], ant_locs[0][1] - vector[1])
  an2 = (ant_locs[1][0] + vector[0], ant_locs[1][1] + vector[1])
  return (an1, an2)

def get_harmonic_antinodes(ant_locs, map):
  vector = (ant_locs[1][0] - ant_locs[0][0], ant_locs[1][1] - ant_locs[0][1])
  a_nodes = set()
  # Travel in negative direction
  cur_node = ant_locs[0]
  while(is_in_bounds(cur_node, map)):
    a_nodes.add(cur_node)
    cur_node = (cur_node[0] - vector[0], cur_node[1] - vector[1])
  # Travel in positive direction
  cur_node = ant_locs[0]
  while(is_in_bounds(cur_node, map)):
    a_nodes.add(cur_node)
    cur_node = (cur_node[0] + vector[0], cur_node[1] + vector[1])

  return a_nodes
  
# Adds antinodes for every combination of antenna pairs
def add_antinodes(ant_locs, antinodes, map, harmonic = False):
  combinations = list(itertools.combinations(ant_locs, 2))

  for combo in combinations:
    ans = get_antinodes(combo)
    if harmonic:
      ans = get_harmonic_antinodes(combo, map)
    for an in ans:
      if is_in_bounds(an, map):
        antinodes.add(an)

def main():
  # Read input
  with open("input.txt", "r") as file:
      map = [line.strip() for line in file]

  antennas = dict()
  antinodes = set()

  for y, row in enumerate(map):
    for x, sym in enumerate(row):
      if sym in antennas:
        antennas.get(sym).append((x, y))
      elif sym != ".":
        antennas[sym] = [(x, y)]

  # Part 1
  for ant_locs in antennas.values():
    add_antinodes(ant_locs, antinodes, map)

  print(len(antinodes))

  # Part 2
  for ant_locs in antennas.values():
    add_antinodes(ant_locs, antinodes, map, harmonic=True)

  print(len(antinodes))

main()
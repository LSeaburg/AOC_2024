from queue import PriorityQueue

def turn_left(dir):
  if dir == "^":
    return "<"
  if dir == "<":
    return "v"
  if dir == "v":
    return ">"
  if dir == ">":
    return "^"
  return dir

def turn_right(dir):
  if dir == "^":
    return ">"
  if dir == ">":
    return "v"
  if dir == "v":
    return "<"
  if dir == "<":
    return "^"
  return dir

def walk(pos, dir):
  (x, y) = pos
  if dir == "^":
    return (x, y-1)
  if dir == "v":
    return (x, y+1)
  if dir == "<":
    return (x-1, y)
  if dir == ">":
    return (x+1, y)
  return pos

# Implements BFS with a priority queue
# Keeps seperate dicts for costs and paths of seen elements 
def get_paths(start_orientation, end_pos, barriers):
  investigate = PriorityQueue()
  seen = set()
  seen_costs = dict()
  seen_paths = dict()

  investigate.put((0, start_orientation))
  seen_costs.update({start_orientation: 0})
  seen_paths.update({start_orientation: {start_orientation}})

  # Implment BFS based on cost priority
  while investigate:
    cost, orientation = investigate.get()
    (pos, dir) = orientation
    if pos == end_pos:
      return seen_costs[orientation], seen_paths[orientation]

    # Calculate new orientations/positions to check
    l_dir = turn_left(dir)
    r_dir = turn_right(dir)
    new_pos = walk(pos, dir)

    new_orientations = (((new_pos, dir), 1), 
                        ((pos, l_dir), 1000),
                        ((pos, r_dir), 1000))
    
    for new_orientation, new_cost in new_orientations:
      if not new_orientation in seen and not new_orientation[0] in barriers:
        investigate.put((cost + new_cost, new_orientation))
        seen.add(new_orientation)
        seen_costs.update({new_orientation: cost + new_cost})
        seen_paths.update({new_orientation: seen_paths[orientation] | {new_orientation}})
      # Add paths from different areas that would lead to the same cost to get all squares on optimal paths
      elif new_orientation in seen and seen_costs[new_orientation] == cost + new_cost: 
        seen_paths.update({new_orientation: seen_paths[new_orientation] | seen_paths[orientation]})

  # Default return if there is no path
  return -1, set()

def main():
  # Read input 
  f = open("input.txt")
  input = f.readlines()

  barriers = set()
  for y, rows in enumerate(input):
    for x, sym in enumerate(rows):
      if sym == "#":
        barriers.add((x, y))
      elif sym == "S":
        start_pos = (x, y)
      elif sym == "E":
        end_pos = (x, y)

  # Parts 1 and 2
  cost, paths = get_paths((start_pos, ">"), end_pos, barriers)

  unique_pos = set()
  for item in paths:
    (pos, dir) = item
    unique_pos.add(pos)

  print(cost)
  print(len(unique_pos))

main()
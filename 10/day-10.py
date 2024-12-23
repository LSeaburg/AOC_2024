def is_in_bounds(pos, map):
  if pos[0] < 0 or pos[1] < 0:
    return False
  if pos[0] >= len(map):
    return False
  if pos[1] >= len(map[0]):
    return False
  return True

def get_surrounding_areas(pos, map):
  areas = []
  if is_in_bounds((pos[0]-1, pos[1]), map):
    areas.append((pos[0]-1, pos[1]))
  if is_in_bounds((pos[0]+1, pos[1]), map):
    areas.append((pos[0]+1, pos[1]))
  if is_in_bounds((pos[0], pos[1]-1), map):
    areas.append((pos[0], pos[1]-1))
  if is_in_bounds((pos[0], pos[1]+1), map):
    areas.append((pos[0], pos[1]+1))
  return areas

def find_peak(to_investigate, found_peaks, map):
  next_investigation = set()
  for pos in to_investigate:
    height = map[pos[0]][pos[1]]
    for p in get_surrounding_areas(pos, map):
      if map[p[0]][p[1]] == height + 1:
        next_investigation.add(p)
        if map[p[0]][p[1]] == 9:
          found_peaks.add(p)
  return next_investigation

# Uses list instead of set to keep duplicate values
def find_peak_with_redundant_paths(to_investigate, found_peaks, map):
  next_investigation = []
  for pos in to_investigate:
    height = map[pos[0]][pos[1]]
    for p in get_surrounding_areas(pos, map):
      if map[p[0]][p[1]] == height + 1:
        next_investigation.append(p)
        if map[p[0]][p[1]] == 9:
          found_peaks.append(p)
  return next_investigation

def get_score(trail_head, map):
  to_investigate = set()
  found_peaks = set()
  to_investigate.add(trail_head)

  while len(to_investigate) != 0:
    to_investigate = find_peak(to_investigate, found_peaks, map)
  return len(found_peaks)

def get_rating(trail_head, map):
  to_investigate = []
  found_peaks = []
  to_investigate.append(trail_head)

  while len(to_investigate) != 0:
    to_investigate = find_peak_with_redundant_paths(to_investigate, found_peaks, map)
  return len(found_peaks)

def main():
  # Read input
  top_map = []
  trail_heads = []

  with open("input.txt", "r") as file:
      for line in file:
          top_map.append(list(map(int, line.strip())))

  for i, row in enumerate(top_map):
    for j, height in enumerate(row):
      if height == 0:
        trail_heads.append((i, j))

  # Part 1
  score_total = 0
  for th in trail_heads:
    score_total += get_score(th, top_map)

  print(score_total)

  # Part 2
  rating_total = 0
  for th in trail_heads:
    rating_total += get_rating(th, top_map)

  print(rating_total)

main()
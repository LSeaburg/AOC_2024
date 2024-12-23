from collections import namedtuple
from collections import deque 

Position = namedtuple("Position", ["x", "y"])

def get_neighbors(cur, barriers):
  n = []
  if not Position(cur.x, cur.y + 1) in barriers:
    n.append(Position(cur.x, cur.y + 1))
  if not Position(cur.x, cur.y - 1) in barriers:
    n.append(Position(cur.x, cur.y - 1))
  if not Position(cur.x + 1, cur.y) in barriers:
    n.append(Position(cur.x + 1, cur.y))
  if not Position(cur.x - 1, cur.y) in barriers:
    n.append(Position(cur.x - 1, cur.y))
  return n

# Uses BFS to find a path
def find_path(start, end, barriers):
  to_investigate = deque([(start, [start])])
  seen = set()

  while to_investigate:
    cur, path = to_investigate.popleft()
    neighbors = get_neighbors(cur, barriers)
    for neighbor in neighbors:
      if neighbor not in seen:
        seen.add(neighbor)
        if neighbor == end:
          return path + [neighbor]
        to_investigate.append((neighbor, path + [neighbor]))
  return []

# Uses binary search to find transition from a path existing to a path no longer existing
def find_last_barrier(start, end, corrupted_bytes, borders):
  first = 0
  last = len(corrupted_bytes) - 1
  while last - first > 1:
    mid = int((first + last) / 2)
    if find_path(start, end, borders + corrupted_bytes[:mid]):
      first = mid
    else:
      last = mid
  if find_path(start, end, borders + corrupted_bytes[:first]):
    return corrupted_bytes[first]
  return corrupted_bytes[last]

def main():
  # Read input
  corrupted_bytes = []

  BOUND = 70
  FIRST_BYTES = 1024

  with open("input.txt", "r") as file:
      line = file.readline()
      while line:
        [x, y] = list(map(int, line.strip().split(",")))
        corrupted_bytes.append(Position(x, y))
        line = file.readline()

  barriers = corrupted_bytes[:FIRST_BYTES]
  borders = []

  # Add barriers around map as borders for easy OOB detection
  for i in range(BOUND + 1):
    borders.append(Position(-1, i))
    borders.append(Position(i, -1))
    borders.append(Position(BOUND + 1, i))
    borders.append(Position(i, BOUND + 1))

  start = Position(0, 0)
  end = Position(BOUND, BOUND)

  # Part 1
  path = find_path(start, end, barriers + borders)
  print(len(path) - 1)

  # Part 2
  pos = find_last_barrier(start, end, corrupted_bytes, borders)
  print(str(pos.x) + "," + str(pos.y))

main()
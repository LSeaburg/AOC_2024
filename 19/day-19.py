def is_possible_pattern(pattern, towels):
  if pattern == "":
    return True
  for towel in towels:
    if towel == pattern[:len(towel)]:
      if is_possible_pattern(pattern[len(towel):], towels):
        return True
  return False

# Uses cache/dynamic programming
def get_num_of_arrangements(pattern, towels, arrangements, segs, seen):
  if pattern == "":
    return 1
  if pattern in seen:
    return seen[pattern]
  for towel in towels:
    if towel == pattern[:len(towel)]:
      new_arrangements = get_num_of_arrangements(pattern[len(towel):], towels, 0, segs + [towel], seen)
      arrangements = arrangements + new_arrangements
      seen.update({pattern: arrangements})
  return arrangements

def main():
  # Read input
  towels = []
  patterns = []

  with open("input.txt", "r") as file:
      line = file.readline()
      towel_strs = line.strip().split(",")
      for str in towel_strs:
        towels.append(str.strip())

      line = file.readline()
      line = file.readline()
      while line:
        patterns.append(line.strip())
        line = file.readline()

  # Part 1
  count = 0
  for pattern in patterns:
    if is_possible_pattern(pattern, towels):
      count += 1
  print(count)

  # Part 2
  count = 0
  seen = dict()
  for pattern in patterns:
    count += get_num_of_arrangements(pattern, towels, 0, [], dict())
  print(count)

main()
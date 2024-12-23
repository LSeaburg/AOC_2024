import math

def blink(stones):
  new_stones = []

  for stone in stones:
    if stone == 0:
      new_stones.append(1)
    elif int(math.log10(stone) + 1) % 2 == 0: ## even number of digits
      half = int(math.log10(stone) + 1) / 2
      new_stones.append(int(stone / (10 ** half)))
      new_stones.append(int(stone % (10 ** half)))
    else:
      new_stones.append(stone * 2024)
  return new_stones

# Uses cache to reduce computation
def get_stone_size(stones, iter, seen):
  total_stones = 0
  for stone in stones:
    if (stone, iter) in seen:
      total_stones += seen[(stone, iter)]
    else:
      new_stones = blink([stone])
      if iter == 1:
        new_stone_num = len(new_stones)
      else:
        new_stone_num = get_stone_size(new_stones, iter - 1, seen)
      seen.update({(stone, iter): new_stone_num})
      total_stones += new_stone_num
  return total_stones

def main():
  # Read input
  with open("input.txt", "r") as file:
      for line in file:
          stones = list(map(int, line.strip().split(" ")))

  # Part 1
  print(get_stone_size(stones, 25, dict()))

  # Part 2
  print(get_stone_size(stones, 75, dict()))

main()
def read_lock(input, sym="#"):
  heights = []
  for x in range(5):
    height = 0
    while input[height][x] == sym:
      height += 1
    heights.append(height - 1)
  return tuple(heights)

def read_key(input):
  inverse_key = read_lock(input, sym=".")
  return tuple(5 - h for h in inverse_key)

def key_fits(key, lock):
  for x in range(5):
    if key[x] + lock[x] > 5:
      return False
  return True

def main():
  # Read input 
  locks = set()
  keys = set()

  with open("input.txt", "r") as file:
    line = file.readline().strip()
    while line:
      block = [line]
      for _ in range(6):
        block.append(file.readline().strip())
      if block[0] == "#####":
        locks.add(read_lock(block))
      else:
        keys.add(read_key(block))
      
      line = file.readline().strip() # newline between blocks
      line = file.readline().strip()

  count = 0
  for key in keys:
    for lock in locks:
      if key_fits(key, lock):
        count += 1
  print(count)

main()
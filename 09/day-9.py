def main():
  # Read input
  with open("input.txt", "r") as file:
      disk_map = list(map(int, file.readline().strip()))

  file_space = disk_map[::2]
  free_space = disk_map[1::2]

  real_space = []

  # Build real space block representation
  for i in range(len(file_space) - 1):
    for _ in range(file_space[i]):
      real_space.append(i)
    for _ in range(free_space[i]):
      real_space.append(-1)
  # Handle last one seperately because if mismatched free_space length
  for _ in range(file_space[-1]):
    real_space.append(i+1)

  # Move file block from end to free space at front
  while -1 in real_space:
    i = real_space.index(-1)
    num = -1
    while num == -1:
      num = real_space.pop()
    real_space[i] = num

  checksum = 0
  for i, id in enumerate(real_space):
    checksum += i * id
  print(checksum)

  # Part 2
  file_space = disk_map[::2]
  free_space = disk_map[1::2]

  free_space.append(0)

  # Create list of file spaces, keep track of 
  #   file size, file ID, and free space
  enumerated_file_space = []
  for i, size in enumerate(file_space):
    enumerated_file_space.append([size, i, free_space[i]])

  reordered_enumerated_file_space = enumerated_file_space.copy()

  # Consider every file space in reverse order (decreasing ID)
  for i in range(len(enumerated_file_space) - 1, -1, -1):
    file = enumerated_file_space[i]
    # Check if there is enough free space to move file
    for j, f in enumerate(reordered_enumerated_file_space):
      move_to_index = -1
      if f[1] == file[1]: # Don't move the file backwards
        break
      if f[2] >= file[0]: # Enough free space to move file
        move_to_index = j
        break
    if move_to_index != -1:
      # Find index in the reordered block of the ID block being considered
      index = -1
      for j in range(len(reordered_enumerated_file_space)):
        if reordered_enumerated_file_space[j][1] == file[1]:
          index = j
          break
      # Update freespace
      reordered_enumerated_file_space[index-1][2] = (reordered_enumerated_file_space[index-1][2] +
                                                     reordered_enumerated_file_space[index][2] + 
                                                     reordered_enumerated_file_space[index][0])
      reordered_enumerated_file_space[index][2] = (reordered_enumerated_file_space[move_to_index][2] -
                                                  reordered_enumerated_file_space[index][0])
      # File before insertion will have no more free space
      reordered_enumerated_file_space[move_to_index][2] = 0

      # Move file
      reordered_enumerated_file_space.remove(file)
      reordered_enumerated_file_space.insert(move_to_index + 1, file)

  real_space = []

  # Build real space block representation from the reordered file space
  for file in reordered_enumerated_file_space:
    for _ in range(file[0]):
      real_space.append(file[1])
    for _ in range(file[2]):
      real_space.append(-1)

  checksum = 0
  for i, id in enumerate(real_space):
    if id != -1:
      checksum += i * id

  print(checksum)

main()
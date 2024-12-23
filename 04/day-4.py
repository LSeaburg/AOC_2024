# List of possible orientations of the words XMAS
positions = [
  [[0,0], [0,1], [0,2], [0,3]],
  [[0,3], [0,2], [0,1], [0,0]],
  [[0,0], [1,0], [2,0], [3,0]],
  [[3,0], [2,0], [1,0], [0,0]],
  [[0,0], [1,1], [2,2], [3,3]],
  [[3,3], [2,2], [1,1], [0,0]],
  [[0,3], [1,2], [2,1], [3,0]],
  [[3,0], [2,1], [1,2], [0,3]]
]##  X      M      A      S

# List of possible orientations of mas cross
mas_positions = [
  [[1,1], [0,0], [2,2], [0,2], [2,0]],
  [[1,1], [0,0], [2,2], [2,0], [0,2]],
  [[1,1], [2,2], [0,0], [0,2], [2,0]],
  [[1,1], [2,2], [0,0], [2,0], [0,2]]
]##  A      M      S      M      S

def main():
  # Read input
  f = open("input.txt")
  lines = f.readlines()

  wordsearch = []

  # Add border to prevent out of bounds during search
  for line in lines:
    line = line[:-1] + "..."
    wordsearch.append(list(line))
  dummy_lines = ['.'] * (len(lines[0]) + 2)
  for i in range(3):
    wordsearch.append(dummy_lines)

  # Part 1
  count = 0

  for pos in positions:
    for i in range(len(wordsearch) - 3):
      for j in range(len(wordsearch[0]) - 3):
        # Test if there is a match to an element of the orientation string
        if (wordsearch[i + pos[0][0]][j + pos[0][1]] == "X" and
            wordsearch[i + pos[1][0]][j + pos[1][1]] == "M" and
            wordsearch[i + pos[2][0]][j + pos[2][1]] == "A" and
            wordsearch[i + pos[3][0]][j + pos[3][1]] == "S"):
          count = count + 1

  print(count)

  # Part 2
  mas_count = 0

  for pos in mas_positions:
    for i in range(len(wordsearch) - 3):
      for j in range(len(wordsearch[0]) - 3):
        # Test if there is a match to an element of the mas orientation string
        if (wordsearch[i + pos[0][0]][j + pos[0][1]] == "A" and
            wordsearch[i + pos[1][0]][j + pos[1][1]] == "M" and
            wordsearch[i + pos[2][0]][j + pos[2][1]] == "S" and
            wordsearch[i + pos[3][0]][j + pos[3][1]] == "M" and
            wordsearch[i + pos[4][0]][j + pos[4][1]] == "S"):
          mas_count = mas_count + 1

  print(mas_count)

main()
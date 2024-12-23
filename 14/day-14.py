def add_to_quad(position, quad_count, W, H):
  (x, y) = position
  if x < (W-1)/2 and y < (H-1)/2:
    quad_count[0] += 1
  if x < (W-1)/2 and y > (H-1)/2:
    quad_count[1] += 1
  if x > (W-1)/2 and y < (H-1)/2:
    quad_count[2] += 1
  if x > (W-1)/2 and y > (H-1)/2:
    quad_count[3] += 1
  return

def get_final_positions(positions, steps, W, H):
  final_positions = []

  for position in positions:
    ((px, py), (vx, vy)) = position
    
    x = (px + steps * vx) % W
    y = (py + steps * vy) % H
    final_positions.append((x, y))
  return final_positions

def display_arrangement(positions, W, H):
  for y in range(H):
    for x in range(W):
      if (x, y) in positions:
        print("X", end="")
      else:
        print(".", end="")
    print()
  return

def main():
  # Read input 
  initial_positions = []

  with open("input.txt", "r") as file:
    for line in file:
      vals = line.strip().split(" ")
      p_vals = vals[0].split("=")[1]
      v_vals = vals[1].split("=")[1]

      p = tuple(map(int, p_vals.split(",")))
      v = tuple(map(int, v_vals.split(",")))
      initial_positions.append((p, v))

  # Part 1
  W = 101
  H = 103
  final_positions = get_final_positions(initial_positions, 100, W, H)

  quad_count = [0, 0, 0, 0]

  for position in final_positions:
    add_to_quad(position, quad_count, W, H)

  print(quad_count[0] * quad_count[1] * quad_count[2] * quad_count[3])

  # Part 2

  # for i in range(10000):
  #   final_positions = get_final_positions(initial_positions, i, W, H)
  #   print(i)
  #   display_arrangement(final_positions, W, H)
  #   print()

# After displaying a few hundred patterns, there was a pattern in x/y patterns at regular periods
  ## 1 + 103y
  ## 46 + 101x

  # Solve for integers where the above equations intersect
  for i in range(100):
    num = 1 + 103 * i
    candidate = (num - 46) / 101
    if candidate.is_integer():
      print(num)

  final_positions = get_final_positions(initial_positions, 7520, W, H)
  display_arrangement(final_positions, W, H)

main()
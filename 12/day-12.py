def is_in_bounds(pos, map):
  if pos[0] < 0 or pos[1] < 0:
    return False
  if pos[0] >= len(map):
    return False
  if pos[1] >= len(map[0]):
    return False
  return True

def get_surrounding_plants(pos, map, oob = False):
  areas = []
  if is_in_bounds((pos[0]-1, pos[1]), map) or oob:
    areas.append((pos[0]-1, pos[1]))
  if is_in_bounds((pos[0]+1, pos[1]), map) or oob:
    areas.append((pos[0]+1, pos[1]))
  if is_in_bounds((pos[0], pos[1]-1), map) or oob:
    areas.append((pos[0], pos[1]-1))
  if is_in_bounds((pos[0], pos[1]+1), map) or oob:
    areas.append((pos[0], pos[1]+1))
  return areas

def get_plant(pos, garden):
  return garden[pos[0]][pos[1]]

def add_to_plot(plant, plot, to_check, garden):
  next_check = set()
  for pos in to_check:
    if get_plant(pos, garden) == plant:
      plot.add(pos)
      for p in get_surrounding_plants(pos, garden):
        if p not in plot:
          next_check.add(p)
  return next_check

# Returns a full plot of the same plant as a set of coordinates
def find_plot(pos, garden):
  plot = set()
  to_check = set({pos})
  plant = get_plant(pos, garden)

  while len(to_check) != 0:
    to_check = add_to_plot(plant, plot, to_check, garden)
  return plot

def get_area(plot):
  return len(plot)

def get_perimeter(plot, garden):
  perimeter = 0
  for pos in plot:
    sur = get_surrounding_plants(pos, garden)
    perimeter += 4 - len(sur)
    for p in sur:
      if get_plant(pos, garden) != get_plant(p, garden):
        perimeter += 1
  return perimeter

# Returns every side unit as a vector of two coordinates to the bordering 
#   plot unit to the outer plot unit
def get_side_units(plot, garden):
  side_units = set()
  for pos in plot:
    sur = get_surrounding_plants(pos, garden, True)
    for p in sur:
      if not is_in_bounds(p, garden) or get_plant(pos, garden) != get_plant(p, garden):
        side_units.add((pos, p))
  return side_units

# Retruns True if side units are adjecent and in the same direction
def side_is_adjacent(s1, s2):
  vecs = {(-1, 0), (1, 0), (0, -1), (0, 1)}
  for v in vecs:
    if (s2[0] == tuple(a + b for a, b in zip(s1[0], v)) and
        s2[1] == tuple(a + b for a, b in zip(s1[1], v))):
      return True
  return False

# Creates all side units for a plot and groups them together into sides
def get_sides(plot, garden):
  side_units = get_side_units(plot, garden)
  sides = []
  for side_unit in side_units:
    adj_sides = []
    for s_index, side in enumerate(sides):
      for su in side:
        if side_is_adjacent(side_unit, su):
          adj_sides.append(s_index)
    if len(adj_sides) == 0:
      sides.append([side_unit])
    elif len(adj_sides) == 1:
      sides[adj_sides[0]].append(side_unit)
    else: ## len(found_sides) == 2
      sides[adj_sides[0]].append(side_unit)
      sides[adj_sides[0]].extend(sides[adj_sides[1]])
      sides.pop(adj_sides[1])
  return len(sides)

def main():
  # Read input
  garden = []

  with open("input.txt", "r") as file:
      for line in file:
          garden.append(line.strip())

  plots = []
  added_to_plot = set()

  for i, row in enumerate(garden):
    for j, plant in enumerate(row):
      pos = (i, j)

      if pos not in added_to_plot:
        new_plot = find_plot(pos, garden)
        plots.append(new_plot)
        added_to_plot.update(new_plot)

  # Part 1
  cost = 0
  for plot in plots:
    cost += get_area(plot) * get_perimeter(plot, garden)
  print(cost)

  # Part 2
  new_cost = 0
  for plot in plots:
    new_cost += get_area(plot) * get_sides(plot, garden)
  print(new_cost)

main()
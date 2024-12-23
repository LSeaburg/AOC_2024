# Returns True if every page's depencendy has been seen in 
#  the order prior to the pages appearance in the order
def is_valid(order, dependencies):
  seen = set()
  for page in order:
    if page in dependencies:
      for dependency in dependencies[page]:
        if dependency in seen:
          return False
    seen.add(page)
  return True

# If the list is valid returns the midpoint value of the list
def check_order(order, dependencies):
  if is_valid(order, dependencies):
    midpoint = int(len(order)/2)
    return order[midpoint]
  return 0

# Changes the position of the first invalid page with the position of it's dependency
def swap_pages(order, dependencies):
  seen = dict()
  for index, page in enumerate(order):
    if page in dependencies:
      for dependency in dependencies[page]:
        if dependency in seen:
          new_order = order.copy()
          new_order[index] = dependency
          new_order[seen[dependency]] = page
          return new_order
    seen.update({page: index})
  return order

# Swap page orders until the order is valid
def fix_order(order, dependencies):
  while not is_valid(order, dependencies):
    order = swap_pages(order, dependencies)
  return order

# If the page order is incorrect, returns the midpoint value of the corrected order
def check_incorrect_order(order, dependencies):
  if is_valid(order, dependencies):
    return 0
  new_order = fix_order(order, dependencies)
  midpoint = int(len(new_order)/2)
  return new_order[midpoint]

def main():
  # Read in file
  rules = []
  orders = []

  with open("input.txt", "r") as file:
    # Reads in page ordering rules
    line = file.readline()
    while line != "\n":
      rule = list(map(int, line.strip().split('|')))
      rules.append(rule)
      line = file.readline()

    # Reads in page orders
    line = file.readline()
    while (line):
      order = list(map(int, line.split(',')))
      orders.append(order)
      line = file.readline()

  # Creates dependency data structure
  dependencies = dict()
  for rule in rules:
    if dependencies.get(rule[0]):
      dependencies[rule[0]].add(rule[1])
    else:
      dependencies[rule[0]] = {rule[1]}

  # Part 1
  sum = 0
  for order in orders:
    sum += check_order(order, dependencies)
  print(sum)

  # Part 2
  sum = 0
  for order in orders:
    sum = sum + check_incorrect_order(order, dependencies)
  print(sum)

main()
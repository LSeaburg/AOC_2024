import collections

Position = collections.namedtuple("Position", ("x", "y"))

numeric_keypad = dict({
  "A": Position(2, 3),
  "0": Position(1, 3),
  "1": Position(0, 2),
  "2": Position(1, 2),
  "3": Position(2, 2),
  "4": Position(0, 1),
  "5": Position(1, 1),
  "6": Position(2, 1),
  "7": Position(0, 0),
  "8": Position(1, 0),
  "9": Position(2, 0),
  "gap": Position(0, 3)
})

directional_keypad = dict({
  "A": Position(2, 0),
  "^": Position(1, 0),
  "v": Position(1, 1),
  "<": Position(0, 1),
  ">": Position(2, 1),
  "gap": Position(0, 0)
})

# Greedy algorithm works for simple problem but does not work for large depths
def get_keypresses(code, keypad):
  presses = ""
  cur = keypad["A"]

  for key in code:
    pos = keypad[key]
    up_right = False
    difference = Position(pos.x - cur.x, pos.y - cur.y)
    down_right = difference.y > 0 and difference.x > 0
    
    if (keypad["gap"] == Position(pos.x, cur.y) or   # can't go left first because gap
       (down_right and keypad["gap"] != Position(cur.x, pos.y))):
      presses += "^" * (-1 * difference.y)
      presses += "v" * difference.y
      presses += "<" * (-1 * difference.x)
      presses += ">" * difference.x
    else:
      presses += "<" * (-1 * difference.x)
      presses += ">" * difference.x
      presses += "^" * (-1 * difference.y)
      presses += "v" * difference.y
    presses += "A"
    cur = pos

  return presses

def get_possible_keypresses(code, keypad):
  presses = [""]
  cur = keypad["A"]

  for key in code:
    pos = keypad[key]
    difference = Position(pos.x - cur.x, pos.y - cur.y)
    dupe_presses = []
    for i in range(len(presses)):
      # Only move vert then horz if moving horz first 
      #   would cross a gap
      if (keypad["gap"] == Position(pos.x, cur.y)):
        presses[i] += "^" * (-1 * difference.y)
        presses[i] += "v" * difference.y
        presses[i] += "<" * (-1 * difference.x)
        presses[i] += ">" * difference.x
      else:
        # Check if we need to check both v/h and h/v
        # If we are only moving in one direction, we don't need 2 options
        # If moving v then h would cross a gap, we don't need 2 options
        # Else add both options as possible
        if (difference.x != 0 and difference.y != 0 and 
            (keypad["gap"] != Position(cur.x, pos.y))):
          dupe_press = presses[i]
          dupe_press += "^" * (-1 * difference.y)
          dupe_press += "v" * difference.y
          dupe_press += "<" * (-1 * difference.x)
          dupe_press += ">" * difference.x
          dupe_press += "A"
          dupe_presses.append(dupe_press)
        
        presses[i] += "<" * (-1 * difference.x)
        presses[i] += ">" * difference.x
        presses[i] += "^" * (-1 * difference.y)
        presses[i] += "v" * difference.y
      presses[i] += "A"
    presses += dupe_presses
    cur = pos

  return presses

# Does the inverse of getting the key_presses
# Used for debugging
def simulate_presses(code, keypad):
  reverse_keypresses = {v: k for k, v in keypad.items()}

  presses = ""
  cur = keypad["A"]

  for move in code:
    if move == "^":
      cur = Position(cur.x, cur.y-1)
    elif move == "v":
      cur = Position(cur.x, cur.y+1)
    elif move == "<":
      cur = Position(cur.x-1, cur.y)
    elif move == ">":
      cur = Position(cur.x+1, cur.y)
    elif move == "A":
      presses += reverse_keypresses[cur]
    
  return presses

def get_numeric_code(code):
  return int(code[:-1])

# Converts string of codes into list of strings ending at every 'A'
def get_sub_codes(code):
  str_pointer = 0
  sub_codes = []

  while str_pointer < len(code):
    next_occr = code.find("A", str_pointer)
    sub_codes.append(code[str_pointer:next_occr + 1])
    str_pointer = next_occr + 1

  return sub_codes

# Dynamic programming check for shortest sequence
# Examine all possible sequences
def shortest_sequence(code, keypad, depth, seen):
  if depth == 0:
    return len(code)
  if (code, depth) in seen:
    return seen[(code, depth)]
  
  length = 0
  for sub_code in get_sub_codes(code):
    sub_code_lengths = []
    poss_seqs = get_possible_keypresses(sub_code, keypad)
    for poss_seq in poss_seqs:
      sub_code_lengths.append(shortest_sequence(poss_seq, keypad, depth - 1, seen))
    length += min(sub_code_lengths)

  seen.update({(code, depth): length})
  return length
  
def main():
  # Read input
  codes = []
  with open("input.txt", "r") as file:
    line = file.readline()
    while line:
      codes.append(line.strip())
      line = file.readline()

  # Part 1
  complexity = 0
  for code in codes:
    press_seq = []
    press_seq.append(get_keypresses(code, numeric_keypad))
    for i in range(2):
      press_seq.append(get_keypresses(press_seq[i], directional_keypad))

    length = len(press_seq[-1])
    complexity += length * get_numeric_code(code)
  print(complexity)

  # Part 2
  total = 0
  cache = dict()

  for code in codes:
    poss_num_codes = get_possible_keypresses(code, numeric_keypad)

    lengths = []
    for poss_num_code in poss_num_codes:
      lengths.append(shortest_sequence(poss_num_code, directional_keypad, 25, cache))

    total += min(lengths) * get_numeric_code(code)
  print(total)

main()
# Returns the value of the combo type operand
def get_combo_operand(operand, registers):
  if operand == 4:
    return registers[0]
  if operand == 5:
    return registers[1]
  if operand == 6:
    return registers[2]
  return operand

# Gives the output of the program according to the description
def get_output(a, b, c, program):
  registers = [a, 0, 0]
  ins_pointer = 0
  out = ""
  instructions = list(zip(program[::2], program[1::2]))

  while ins_pointer < len(instructions):
    (opcode, operand) = instructions[ins_pointer]
    if opcode == 0:
      registers[0] = int(registers[0] / (2 ** get_combo_operand(operand, registers)))
    elif opcode == 1:
      registers[1] = registers[1] ^ operand
    elif opcode == 2:
      registers[1] = get_combo_operand(operand, registers) % 8
    elif opcode == 3:
      ins_pointer = ins_pointer + 1 if registers[0] == 0 else operand
    elif opcode == 4:
      registers[1] = registers[1] ^ registers[2]
    elif opcode == 5:
      out = out + str(get_combo_operand(operand, registers) % 8) + ","
    elif opcode == 6:
      registers[1] = int(registers[0] / (2 ** get_combo_operand(operand, registers)))
    elif opcode == 7:
      registers[2] = int(registers[0] / (2 ** get_combo_operand(operand, registers)))

    if opcode != 3:
      ins_pointer = ins_pointer + 1

  return out[:-1]

# Returns the output of the program for a given value of a
def get_output_as_list(a, program):
  out = get_output(a, 0, 0, program)
  return list(map(int, out.split(","))) 

# Converts a list representing a base-8 number (in reverse) to decimal
def exponize(lst):
  sum = 0
  for i, num in enumerate(lst):
    sum += num * (8 ** i)
  return sum

# Iterates base-8 number, 1 digit at a time, right-to-left
# Finds a match of test output to target output for rightmost numer
#   and move onto the next number
def find_match(program):
  length = len(program)
  a_lst = [0] * len(program)
  a_lst[length - 1] = 1

  out = get_output_as_list(exponize(a_lst), program)
  pointer = length - 1
  while pointer >= 0 and pointer < length:
    out = get_output_as_list(exponize(a_lst), program)
    if out[pointer] == program[pointer]:
      pointer = pointer - 1
    else:
      if a_lst[pointer] == 7:
        a_lst[pointer] = 0
        pointer = pointer + 1
      a_lst[pointer] = a_lst[pointer] + 1

  if pointer == length:
    return -1
  return exponize(a_lst)

def main():
  # Read input
  registers = [0, 0, 0]
  program = []
  instructions = []

  with open("input.txt", "r") as file:
      line = file.readline()
      registers[0] = int(line.split(":")[1].strip())
      line = file.readline()
      registers[1] = int(line.split(":")[1].strip())
      line = file.readline()
      registers[2] = int(line.split(":")[1].strip())
      line = file.readline()
      line = file.readline()
      program = list(map(int, line.split(":")[1].strip().strip().split(",")))

  # Part 1
  out = get_output(registers[0], registers[1], registers[2], program)
  print(out)

  # Part 2
  print(find_match(program))

main()
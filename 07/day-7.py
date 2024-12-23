import math

def valid_test_case(test_val, op_vals):
  if len(op_vals) == 2:
    return ((op_vals[0] * op_vals[1] == test_val) or 
            (op_vals[0] + op_vals[1] == test_val))
  mul_op_vals = [op_vals[0] * op_vals[1]] + op_vals[2:]
  sum_op_vals = [op_vals[0] + op_vals[1]] + op_vals[2:]
  return (valid_test_case(test_val, mul_op_vals) or 
          valid_test_case(test_val, sum_op_vals))

def concat(num1, num2):
  power = math.log10(num2)
  return num1 * (10 ** (int(power) + 1)) + num2

def valid_test_case_with_concat(test_val, op_vals):
  if len(op_vals) == 2:
    return ((op_vals[0] * op_vals[1] == test_val) or 
            (op_vals[0] + op_vals[1] == test_val) or
            (concat(op_vals[0], op_vals[1]) == test_val))
  mul_op_vals = [op_vals[0] * op_vals[1]] + op_vals[2:]
  sum_op_vals = [op_vals[0] + op_vals[1]] + op_vals[2:]
  cat_op_vals = [concat(op_vals[0], op_vals[1])] + op_vals[2:]
  return (valid_test_case_with_concat(test_val, mul_op_vals) or 
          valid_test_case_with_concat(test_val, sum_op_vals) or
          valid_test_case_with_concat(test_val, cat_op_vals))

def main():
  # Read input
  test_vals = []

  with open("input.txt", "r") as file:
    for line in file:
      vals = line.strip().split(":")
      test_val = int(vals[0])
      op_vals = list(map(int, vals[1].strip().split(" ")))
      test_vals.append([test_val, op_vals])

  # Part 1
  valid_test_total = 0

  for [test_val, op_vals] in test_vals:
    if valid_test_case(test_val, op_vals):
      valid_test_total += test_val

  print(valid_test_total)

  # Part 2
  valid_test_total_with_concat = 0

  for [test_val, op_vals] in test_vals:
    if valid_test_case_with_concat(test_val, op_vals):
      valid_test_total_with_concat += test_val

  print(valid_test_total_with_concat)

main()
import re

# Extracts the numbers from the instruction
def process_mul_instruction(s):
  nums = list(map(int, s[4:-1].split(',')))
  return nums[0] * nums[1]

def process_instruction(s, enabled):
  if s == "do()":
    return [0, True]
  elif s == "don't()" or enabled == False:
    return [0, False]
  return [process_mul_instruction(s), enabled]

def main():
  # Read input  
  f = open("input.txt")
  lines = f.readlines()

  # Part 1
  pattern = r"mul\(\d+,\d+\)"
  sum = 0
  for line in lines:
    for match in re.findall(pattern, line):
      sum = sum + process_mul_instruction(match)

  print(sum)
      
  # Part 2
  pattern = r"mul\(\d+,\d+\)|do\(\)|don't\(\)"
  uncorrupted_sum = 0
  enabled = True

  for line in lines:
    for match in re.findall(pattern, line):
      [result, enabled] = process_instruction(match, enabled)
      uncorrupted_sum = uncorrupted_sum + result

  print(uncorrupted_sum)

main()
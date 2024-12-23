def is_safe_inc(report):
  for i in range(len(report) - 1):
    k = report[i + 1] - report[i]
    if k < 1 or k > 3:
      return False
  return True

def is_safe_dec(report):
  for i in range(len(report) - 1):
    k = report[i + 1] - report[i]
    if k > -1 or k < -3:
      return False
  return True

def is_safe(report):
  if is_safe_inc(report) or is_safe_dec(report):
    return True
  return False

# Finds if a list is safe with an item removed
def is_safe_dampened(report):
  for i in range(len(report)):
    temp_list = report.copy()
    del(temp_list[i])
    if is_safe(temp_list):
      return True
  return False

def main():
  # Read input
  reports = []
  with open("input.txt", "r") as file:
    line = file.readline().strip()
    while line:
      reports.append(list(map(int, line.split())))
      line = file.readline().strip()

  # Part 1
  num_safe = 0
  for report in reports:
    if (is_safe(report)):
      num_safe = num_safe + 1

  print(num_safe)

  # Part 2
  num_safe_dampened = 0
  for report in reports:
    if (is_safe_dampened(report)):
      num_safe_dampened = num_safe_dampened + 1

  print(num_safe_dampened)

main()
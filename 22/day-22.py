def mix(secret, val):
  return val ^ secret

def prune(secret):
  return secret % 16777216

def generate_secret(num):
  stage_one_secret = prune(mix(num * 64, num))
  stage_two_secret = prune(mix(int(stage_one_secret / 32), stage_one_secret))
  return prune(mix(stage_two_secret * 2048, stage_two_secret))

def main():
  # Read input
  buyer_secrets = []
  with open("input.txt", "r") as file:
    line = file.readline()
    while line:
      buyer_secrets.append(int(line.strip()))
      line = file.readline()

  # Part 1
  total = 0
  for buyer_secret in buyer_secrets:
    secret = buyer_secret
    for _ in range(2000):
      secret = generate_secret(secret)
    total += secret
  print(total)

  # Part 2
  # Create list of what sales would be for every combination of 4 sales
  # Add every transaction to dict where key is the past 4 changes
  total_sales = dict()

  for buyer_secret in buyer_secrets:
    secret = buyer_secret
    prices = [secret % 10]
    diffs = []
    seen = set()
    for _ in range(2000):
      new_secret = generate_secret(secret)
      prices.append(new_secret % 10)
      diffs.append(prices[-1] - prices[-2])
      if len(diffs) >= 4:
        sequence = (diffs[-4], diffs[-3], diffs[-2], diffs[-1])
        if sequence not in seen:
          seen.add(sequence)
          if sequence in total_sales:
            total_sales[sequence] += prices[-1]
          else:
            total_sales[sequence] = prices[-1]
      secret = new_secret

  print(max(total_sales.values()))

main()
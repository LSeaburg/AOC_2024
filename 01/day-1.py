import numpy as np
import pandas as pd

def main():
  # Process Input
  df = pd.read_csv("input.txt", sep="\s+", header=None, names=['Col1', 'Col2'])

  list1 = df["Col1"].to_list()
  list2 = df["Col2"].to_list()
  list1.sort(); list2.sort()

  # Part 1
  l1_distance = np.sum(np.abs(np.array(list1) - np.array(list2)))
  print(l1_distance)

  # Part 2
  freq = dict()
  for num in list2:
    if freq.get(num):
      freq[num] = freq[num] + 1
    else:
      freq[num] = 1

  sim_score = 0
  for num in list1:
    occurences = freq[num] if freq.get(num) else 0
    sim_score += num * occurences

  print(sim_score)

main()
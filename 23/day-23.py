from typing import Set, Tuple

# Adds edges between two nodes
def add_edge(graph, nodes):
  [node1, node2] = nodes

  if node1 in graph:
    graph[node1].add(node2)
  else:
    graph.update({node1: {node2}})

  if node2 in graph:
    graph[node2].add(node1)
  else:
    graph.update({node2: {node1}})

# Returns tuples of all 3-cliques
# Could also be impleted through bron_kerbosch() call
def find_three_clique(graph):
  cliques = set()
  for v1 in graph:
    for v2 in graph[v1]:
      for v3 in graph[v2]:
        if v3 in graph[v1]:
          cliques.add(tuple(sorted([v1, v2, v3])))
  return cliques

# Taken from online
# Returns iterator of all cliques in the graph
def bron_kerbosch(R, P, X, graph):
  if not P and not X:
    yield R
  while P:
    v = P.pop()
    yield from bron_kerbosch(
      R.union({v}),
      P.intersection(graph[v]),
      X.intersection(graph[v]),
      graph
    )
    X.add(v)

def main():
  # Read input
  graph = dict()
  with open("input.txt", "r") as file:
    line = file.readline()
    while line:
      add_edge(graph, line.strip().split("-"))
      line = file.readline()

  # Part 1
  cliques = find_three_clique(graph)

  count = 0
  for clique in cliques:
    t_node = False
    for node in clique:
      if node[0] == "t":
        t_node = True
    if t_node:
      count += 1
  print(count)

  # Part 2
  all_cliques = bron_kerbosch(set(), set(graph.keys()), set(), graph)
  max_clique = max(all_cliques, key=len)

  sorted_mc = sorted(max_clique)
  str = ""
  for name in sorted_mc:
    str += name + ","

  print(str[:-1])

main()
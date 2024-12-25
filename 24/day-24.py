from collections import deque
from itertools import combinations

def get_wire_val(w1, w2, logic):
  if logic == "AND":
    return w1 & w2
  if logic == "OR":
    return w1 | w2
  if logic == "XOR":
    return w1 ^ w2
  Exception("Logic command not reconigzed")

def read_input():
  wire_vals = dict()
  wire_connections = deque()
  max_z = 0

  with open("input.txt", "r") as file:
    # Read initial values
    line = file.readline().strip()
    while line:
      vals = line.split(":")
      wire_vals.update({vals[0]: int(vals[1].strip())})
      line = file.readline().strip()

    # Read equations
    line = file.readline().strip()
    while line:
      vals = line.split(" ")
      wire_connections.append((vals[0], vals[1], vals[2], vals[4]))
      if vals[4][0] == "z":
        z_int = int(vals[4][1:])
        max_z = max(max_z, z_int)
      line = file.readline().strip()
      
  return wire_vals, wire_connections, max_z

# Solves all wires in network
def solve_wires(wire_vals, _wire_connections):
  wire_connections = _wire_connections.copy()
  while wire_connections:
    (wire1, logic, wire2, result) = wire_connections.popleft()
    if wire1 in wire_vals and wire2 in wire_vals:
      wire_vals.update({result : get_wire_val(wire_vals[wire1], wire_vals[wire2], logic)})
    else:
      wire_connections.append((wire1, logic, wire2, result))
  return

# Sets values on x and y wires
def set_wire(value, wire, length, wire_vals):
  bin_str = bin(value)[2:]
  for i in range(length):
    bit = 0 if i > len(bin_str) - 1 else int(bin_str[-i - 1])
    wire_str = wire + "0" + str(i) if i < 10 else wire + str(i)
    wire_vals.update({wire_str : bit})

# Gets the value on an x, y, or z wire
def get_total_wire_val(wire, length, wire_vals):
  total = 0
  for i in range(length):
    wire_str = wire + "0" + str(i) if i < 10 else wire + str(i)
    total += wire_vals[wire_str] * (2 ** i)
  return total

def test_wire_addition(x, y, length, wire_connections):
  wire_vals = dict()
  set_wire(x, "x", length, wire_vals)
  set_wire(y, "y", length, wire_vals)
  solve_wires(wire_vals, wire_connections)
  z = get_total_wire_val("z", length + 1, wire_vals)
  return z == x + y

# Collection of test cases to run against a wire network
def test_level(val, length, wire_connections):
  return (test_wire_addition(int(2 ** (val-1)), int(2 ** (val-1)), length, wire_connections) and
          test_wire_addition(2 ** val, 0, length, wire_connections) and
          test_wire_addition(0, 2 ** val, length, wire_connections) and
          test_wire_addition(2 ** val, 2 ** val, length, wire_connections) and
          test_wire_addition(2 ** (val+1) - 1, 2 ** (val) - 1, length, wire_connections) and
          test_wire_addition(2 ** (val) - 1, 2 ** (val+1) - 1, length, wire_connections))

def dfs(u, graph):
  reach = graph[u] | {u}
  for v in graph[u]:
    reach = reach | dfs(v, graph)
  return reach

def swap_wires(pair, wire_connections, inverse_graph):
  (w1, w2) = pair
  if w1 == w2:
    return
  # This will make wires recursive and unsolvable
  if w2 in dfs(w1, inverse_graph) or w1 in dfs(w2, inverse_graph):
    return
  
  c1 = None
  c2 = None
  for connecition in wire_connections:
    if connecition[3] == w1:
      c1 = connecition
    if connecition[3] == w2:
      c2 = connecition
  if not c1 or not c2:
    return

  new_c1 = (c1[0], c1[1], c1[2], c2[3])
  new_c2 = (c2[0], c2[1], c2[2], c1[3])

  wire_connections.remove(c1)
  wire_connections.remove(c2)
  wire_connections.append(new_c1)
  wire_connections.append(new_c2)

# Add edge to directed graph
def add_edge(u, v, graph):
  if u in graph:
    graph[u].add(v)
  else:
    graph.update({u: {v}})
  if v not in graph:
    graph.update({v: set()})

def calculate_graphs(wire_connections):
  # Create directed graphs of wire inputs
  graph = dict()
  reverse_graph = dict()

  for connection in wire_connections:
    (wire1, _, wire2, result) = connection

    add_edge(wire1, result, graph)
    add_edge(wire2, result, graph)
    add_edge(result, wire1, reverse_graph)
    add_edge(result, wire2, reverse_graph)

  return graph, reverse_graph

# Gets wires between inputs and outputs at a level
def get_intermediate_wires(num, graph, inverse_graph):
  level_0 = "0" + str(num) if num < 10 else str(num)
  level_1 = "0" + str(num+1) if num < 10 + 1 else str(num + 1)

  forward = dfs("x" + level_0, graph) | dfs("y" + level_0, graph)
  lookback = dfs("z" + level_0, inverse_graph) | dfs("z" + level_1, inverse_graph)

  return (forward) & lookback

def main():
  # Read input
  wire_vals, wire_connections, length = read_input()

  # Part 1
  solve_wires(wire_vals, wire_connections)
  print(get_total_wire_val("z", length + 1, wire_vals))

  # Part 2
  swapped = []

  for i in range(length):
    if not test_level(i, length, wire_connections):
      
      graph, inverse_graph = calculate_graphs(wire_connections)
      test_swap = get_intermediate_wires(i, graph, inverse_graph)
      
      # swap wires
      for pair in combinations(test_swap, 2):
        swap_wires(pair, wire_connections, inverse_graph)
        if not (test_level(i, length, wire_connections) and 
                test_level(i+1, length, wire_connections)):
          # Set wires back
          swap_wires(pair, wire_connections, inverse_graph)
        else:
          swapped += pair
          break

  # Format answer
  ans_str = ""
  for wire in sorted(swapped):
    ans_str += wire + ","
  print(ans_str[:-1])

main()
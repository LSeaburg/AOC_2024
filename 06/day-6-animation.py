from typing import Set, Tuple
import time

def is_vertical_direction(dir : str) -> bool:
  return dir == "^" or dir == "v"

def is_horizontal_direction(dir : str) -> bool:
  return dir == "<" or dir == ">"

class Position:
  def __init__(self, x : int, y : int):
    self.x = x
    self.y = y

  def get_x(self) -> int:
    return self.x
  
  def get_y(self) -> int:
    return self.y

  def __eq__(self, value):
    if self.x == value.x and self.y == value.y:
      return True
    return False
  
  def __repr__(self):
    return "Item(%s, %s)" % (self.x, self.y)
  
  def __hash__(self):
    return hash(self.__repr__())

  def __str__(self):
    return "(" + str(self.x) + "," + str(self.y) + ")"
  
class Map:
  def __init__(self, input : str):

    barriers = set()
    for y, rows in enumerate(input):
      for x, sym in enumerate(rows):
        if sym == "#":
          barriers.add(Position(x, y))

    self.width = len(input[0].strip())
    self.height = len(input)
    self.barriers = barriers
    self.virtual_barriers = set()

  def get_width(self) -> int:
    return self.width
  
  def get_height(self) -> int:
    return self.height
  
  def get_barriers(self) -> Set[Position]:
    return self.barriers
  
  def set_virtual_barrier(self, pos : Position) -> None:
    if not self.is_barrier(pos):
      self.virtual_barriers.add(pos)

  def remove_virtual_barrier(self, pos : Position) -> None:
    self.virtual_barriers.remove(pos)

  def get_virtual_barrier(self) -> Set[Position]:
    return self.virtual_barriers
  
  def reset(self) -> None:
    self.virtual_barriers = set()

  def is_barrier(self, pos : Position) -> bool:
    if pos in self.barriers:
      return True
    if pos in self.virtual_barriers:
      return True
    return False
  
  def is_in_bounds(self, pos : Position) -> bool:
    if pos.x < 0:
      return False
    if pos.y < 0:
      return False
    if pos.x >= self.width:
      return False
    if pos.y >= self.height:
      return False
    return True
  
class Guard:
  def __init__(self, position : Position, direction : str):
    self.pos = position
    self.dir = direction

  def set(self, pos : Position, dir : str) -> None:
    self.pos = pos
    self.dir = dir

  def get_position(self) -> Position:
    return self.pos
  
  def get_direction(self) -> str:
    return self.dir

  def forward_position(self) -> Position:
    if self.dir == "^":
      return Position(self.pos.get_x(), self.pos.get_y() - 1)
    if self.dir == "v":
      return Position(self.pos.get_x(), self.pos.get_y() + 1)
    if self.dir == "<":
      return Position(self.pos.get_x() - 1, self.pos.get_y())
    if self.dir == ">":
      return Position(self.pos.get_x() + 1, self.pos.get_y())
    return self.pos
  
  def dir_after_turn(self) -> str:
    if self.dir == "^":
      return ">"
    elif self.dir == ">":
      return "v"
    elif self.dir == "v":
      return "<"
    elif self.dir == "<":
      return "^"

  def next_position(self, map: Map) -> Tuple[Position, str]:
    if map.is_barrier(self.forward_position()):
      return (self.pos, self.dir_after_turn())
    else:
      return (self.forward_position(), self.dir)

  def move(self, map : Map) -> None:
    (self.pos, self.dir) = self.next_position(map)

def create_guard_from_input(input : str) -> Guard:
  directions = ("^", "v", "<", ">")
  for y, rows in enumerate(input):
    for x, sym in enumerate(rows):
      if sym in directions:
        return Guard(Position(x, y), sym)
      
class History:
  def __init__(self):
    self.visited = set()
    self.v_visited = set()
    self.h_visited = set()
    self.prior_guard_states = set()

  def get_visited(self) -> Set[Position]:
    return self.visited
  
  def get_v_visited(self) -> Set[Position]:
    return self.v_visited
  
  def get_h_visited(self) -> Set[Position]:
    return self.h_visited
  
  def get_prior_guard_states(self) -> Set[Position]:
    return self.prior_guard_states

  def reset(self) -> None:
    self.visited = set()
    self.v_visited = set()
    self.h_visited = set()
    self.prior_guard_states = set()
  
  def visit(self, pos : Position, dir : str) -> None:
    self.prior_guard_states.add((pos, dir))
    self.visited.add(pos)
    if is_vertical_direction(dir):
      self.v_visited.add(pos)
    else:
      self.h_visited.add(pos)

class Scene:
  def __init__(self, input : str):

    self.map = Map(input)
    self.guard = create_guard_from_input(input)
    self.history = History()
    self.initial_guard_pos = self.guard.get_position()
    self.initial_guard_dir = self.guard.get_direction()
    
    self.history.visit(self.guard.get_position(), self.guard.get_direction())
    self.draw()
    # self.scene is created by self.draw

  def get_initial_guard_params(self) -> Tuple[Position, str]:
    return (self.initial_guard_pos, self.initial_guard_dir)
  
  def reset(self) -> None:
    self.history.reset()
    self.reset_map() 
    self.reset_guard()

  def reset_guard(self) -> None:
    self.guard.set(self.initial_guard_pos, self.initial_guard_dir)
    self.history.visit(self.guard.get_position(), self.guard.get_direction())

  def reset_map(self) -> None:
    self.map.reset()

  def render(self) -> None:
    CURSOR_UP = "\033[F"

    self.draw()
    print(self)
    print(CURSOR_UP * (self.map.get_height()+1 + 2), end="")
    time.sleep(0.01)

  def draw(self) -> None:
    self.scene = [[" " for _ in range(self.map.get_width())] for _ in range(self.map.get_height())]

    self.draw_barriers()
    self.draw_virtual_barrier()
    self.draw_path()
    self.draw_guard()

  def draw_sym(self, pos : Position, sym : str):
    self.scene[pos.get_y()][pos.get_x()] = sym

  def draw_barriers(self) -> None:
    for pos in self.map.get_barriers():
      self.draw_sym(pos, "#")

  def draw_virtual_barrier(self) -> None:
    for pos in self.map.get_virtual_barrier():
      if self.map.is_in_bounds(pos):
        self.draw_sym(pos, "O")

  def draw_path(self) -> None:
    for pos in self.history.get_visited():
      if self.map.is_in_bounds(pos):
        if pos in self.history.get_h_visited() and pos in self.history.get_v_visited():
          self.draw_sym(pos, "+")
        elif pos in self.history.get_h_visited():
          self.draw_sym(pos, "-")
        else: # pos in self.history.v_visited
          self.draw_sym(pos, "|")

  def draw_guard(self) -> None:
    if self.map.is_in_bounds(self.guard.get_position()):
      self.draw_sym(self.guard.get_position(), self.guard.get_direction())

  def move_guard(self) -> None:
    self.guard.move(self.map)
    self.history.visit(self.guard.get_position(), self.guard.get_direction())

  def contains_guard(self) -> bool:
    return self.map.is_in_bounds(self.guard.get_position())
  
  def add_virtual_barrier(self, pos : Position) -> None:
    if pos == self.guard.get_position():
      return
    self.map.set_virtual_barrier(pos)

  def remove_virtual_barrier(self, pos : Position) -> None:
    self.map.remove_virtual_barrier(pos)
  
  def get_num_of_visited_squares(self) -> int:
    num = 0
    squares = self.history.get_visited()
    for pos in squares:
      if self.map.is_in_bounds(pos):
        num += 1
    return num

  def get_visited_squares(self) -> Set[Position]:
    return self.history.get_visited()
  
  def guard_been_here_before(self) -> bool:
    return (self.guard.next_position(self.map)) in self.history.get_prior_guard_states()
  
  def __str__(self) -> str:
    str = ""
    for _ in range(len(self.scene[0]) + 2):
      str += '%'
    str += '\n'
    for row in self.scene:
      str += "%"
      for sym in row:
        str += sym
      str += "%"
      str += '\n'
    for _ in range(len(self.scene[0]) + 2):
      str += '%'
    str += '\n'
    return str
  
def test_for_loop(scene : Scene) -> bool:
  while scene.contains_guard() and not scene.guard_been_here_before():
    scene.move_guard()

    scene.render()

  return scene.guard_been_here_before()


def main():
  f = open("input2.txt")
  input = f.readlines()

  scene = Scene(input)

  scene.render()
  while scene.contains_guard():
    scene.move_guard()
    scene.render()

  scene.reset_guard()
  scene.render()

  # print(scene.get_num_of_visited_squares())


  candidates = scene.get_visited_squares()

  loop_barriers = set()
  test_scene = Scene(input)

  for pos in candidates:
    test_scene.reset()
    test_scene.add_virtual_barrier(pos)

    if test_for_loop(test_scene):
      loop_barriers.add(pos)
      test_scene.reset_guard()
      test_scene.render()
    
  print(len(loop_barriers))



main()
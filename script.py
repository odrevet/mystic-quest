import re

class Script:
  def __init__(self, id, addr, instructions):
    self.id = id
    self.addr = addr
    self.instructions = instructions


def read_scripts():
  with open("en/scripts/scripts.txt", "r") as file:
      scripts_str = file.read()
      scripts_arr = re.split(
          r"--- script: ([a-f0-9]{4}) addr: ([a-f0-9]{4}) ------------------.*",
          scripts_str,
      )

      variable_declarations = scripts_arr.pop(0)

      scripts = []
      for i in range(0, len(scripts_arr), 3):
          scripts.append(
              Script(scripts_arr[i], scripts_arr[i + 1], scripts_arr[i + 2].strip())
          )

      return variable_declarations, scripts
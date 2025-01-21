from collections.abc import Callable

class Workflow:
  """
  Class representing a Workflow.
  """
  name:str

  def __init__(self, name: str) -> 'Workflow': ...

  def add_task(self, name: str, fn: Callable) -> None:
    """
    Adds a task to the Workflow.
    """
    ...

  def run(self) -> None:
    """
    Runs the Workflow.
    """
    ...

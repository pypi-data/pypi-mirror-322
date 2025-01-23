# kalle
# Copyright (C) 2024 Wayland Holdings, LLC

import sys
from rich.console import Console, Group
from rich.panel import Panel
from rich.syntax import Syntax


class Tool:

  def __init__(self, config):
    self.config = config
    self.console_stderr = Console(file=sys.stderr)

  def key():
    raise NotImplementedError("Subclasses must implement key method")

  def name(self) -> str:
    raise NotImplementedError("Subclasses must implement name method")

  def get_prompt(self) -> str:
    raise NotImplementedError("Subclasses must implement get_prompt method")

  def get_tool_definition(self):
    raise NotImplementedError("Subclasses must implement get_tool_definition method")

  def invoke(self, *args, **kwargs):
    raise NotImplementedError("Subclasses must implement invoke method")

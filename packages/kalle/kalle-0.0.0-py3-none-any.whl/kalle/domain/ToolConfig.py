# kalle
# Copyright (C) 2024 Wayland Holdings, LLC

from pydantic import BaseModel
from typing import Optional, List


class ToolConfig(BaseModel):
  key: str
  class_path: str


class ToolsList(BaseModel):
  tools: List[ToolConfig]

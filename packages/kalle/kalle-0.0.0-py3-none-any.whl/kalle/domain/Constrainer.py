# kalle
# Copyright (C) 2024 Wayland Holdings, LLC

from pydantic import BaseModel
from typing import Optional
from enum import Enum


class ConstrainerType(str, Enum):
  REGEX = "regex"
  JSONSCHEMA = "jsonschema"


class Constrainer(BaseModel):
  type: ConstrainerType
  value: str

# kalle
# Copyright (C) 2024 Wayland Holdings, LLC

from pydantic import BaseModel, model_validator
from typing import Optional


class Uri(BaseModel):
  uri: str
  placeholder: Optional[str] = None
  error: Optional[str] = None
  mime_type: Optional[str] = None
  raw_content: Optional[str] = None
  content_filter: Optional[str] = None

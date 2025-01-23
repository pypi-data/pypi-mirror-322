# kalle
# Copyright (C) 2024 Wayland Holdings, LLC

from pydantic import BaseModel
from typing import Optional

from kalle.domain.ModelConfig import ModelConfig
from kalle.domain.Profile import Profile
from kalle.domain.Prompt import Prompt
from kalle.domain.ToolConfig import ToolsList
from kalle.domain.ModelConfig import ModelConfig
from kalle.domain.Constrainer import Constrainer, ConstrainerType
from kalle.domain.Connector import Connector
from kalle.lib.connectors.LLMConnector import LLMConnector


class LLMRequest(BaseModel):
  key: str
  system_prompt: Optional[Prompt] = None
  piped_prompt: Optional[str] = None
  args_prompt: Optional[str] = None
  tools: Optional[ToolsList] = None
  constrainer: Optional[Constrainer] = None
  connector: Optional[Connector] = None
  model: Optional[ModelConfig] = None

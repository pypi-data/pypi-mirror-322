# kalle
# Copyright (C) 2024 Wayland Holdings, LLC

import random
import time

from rich.console import Console

from openai import OpenAI, InternalServerError, BadRequestError

from . import LLMConnector
from kalle.domain.Prompt import Prompt
from kalle.domain.ModelConfig import ModelParam
from kalle.domain.Constrainer import Constrainer, ConstrainerType

import traceback
import json


class TabbyAPIConnector(LLMConnector.LLMConnector):
  """
  A connector for [TabbyAPI](https://github.com/theroyallab/tabbyAPI), an
  OpenAI compatible exllamav2 API server that's both lightweight and fast.

  It uses the [OpenAI python library[(https://github.com/openai/openai-python).

  Attributes:
      config (dict): The configuration for the connector.
  """

  def __init__(self, config, /, **kwargs):
    """
    Initializes the connector interface.

    Args:
        config (dict): The configuration for the connector.
        **kwargs: Additional keyword arguments.
    """
    super().__init__(config, **kwargs)

  def setup_client(self):
    """
    Sets up the OpenAI client with the provided configuration.
    """
    self.client = OpenAI(
        base_url=self.config["url"],
        api_key=self.config["api_key"],
    )

  def gen_params(self, model_params: list[ModelParam] | None = None, constrainer: Constrainer | None = None) -> dict:
    """
    Generates the model parameters for the API request.

    Args:
        model_params (list[ModelParam] | None): The model parameters.
        constrainer (Constrainer | None): The constrainer.

    Returns:
        dict: The generated parameters.
    """
    if model_params is None:
      return {}

    params = super().gen_params(model_params=model_params)

    # If we have constraints, add them.
    if constrainer is not None:
      extra_body = None
      if constrainer.type == ConstrainerType("jsonschema"):
        extra_body = {"json_schema": json.loads(constrainer.value)}
      if constrainer.type == ConstrainerType("regex"):
        extra_body = {"regex_pattern": constrainer.value}
      params["extra_body"] = extra_body

    return params

  async def request(
      self,
      /,
      system_prompt: str,
      messages: list[dict],
      model_params: list[ModelParam] | None = None,
      constrainer: Constrainer | None = None,
  ) -> str | None:
    """
    Sends a request to the TabbyAPI server.

    Args:
        system_prompt (str): The system prompt.
        messages (list[dict]): The messages.
        model_params (list[ModelParam] | None): The model parameters.
        constrainer (Constrainer | None): The constrainer.

    Returns:
        str | None: The response text or None if the request fails.
    """
    tries = 0
    while tries < self.config["retry_max"]:
      tries += 1
      try:
        seed = None
        gen_params = self.gen_params(model_params=model_params, constrainer=constrainer)

        completion = self.client.chat.completions.create(
            model=self.config["model"],
            messages=[{"role": "system", "content": system_prompt}] + messages,  # type: ignore
            **gen_params,
        )

        response_text = completion.choices[0].message.content
        return response_text

      except BadRequestError as e:
        self.console_stderr.print(f"\n[red]There was an issue with the request: {e}")
        sys.exit(65)

      except InternalServerError as e:
        if self.debug:
          if e.message == "Error code: 502":
            self.console_stderr.print(f"[red]The TabbyAPI server {self.client.base_url} is unreachable.")
          else:
            self.console_stderr.print(f"[red]An exception occurred try {tries} sleeping for {current_delay} {e=}")
            self.console_stderr.print_exception(show_locals=True)
        pass
      except Exception as e:
        if self.debug:
          self.console_stderr.print(f"[red]An exception occurred try {tries} sleeping for {current_delay} {e=}")
          self.console_stderr.print_exception(show_locals=True)
        pass

      current_delay = (
          self.config["retry_delay"]
          * self.config["retry_exponential_base"]
          * (1 + self.config["jitter"] * random.random())
      )

      time.sleep(current_delay)

    return None

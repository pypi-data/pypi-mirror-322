# kalle
# Copyright (C) 2024 Wayland Holdings, LLC

import os
from transformers import AutoTokenizer

from . import BaseTokenizer


class Auto(BaseTokenizer.BaseTokenizer):

  def __init__(self, config, model, tokenizer_key):
    super().__init__(config)
    self.model = model
    self.tokenizer = None

    tokenizer_path = f"../../data/tokenizer_config/{tokenizer_key}"
    tokenizer_path = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), tokenizer_path))
    if os.path.exists(tokenizer_path):
      self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)
    else:
      raise ValueError(f"Invalid tokenizer key: {tokenizer_key}")

  def tokenize(self, text) -> list:
    tokens = self.tokenizer.encode(text) if self.tokenizer is not None else []
    return tokens

  def apply_chat_template(self, conversation: list[dict]) -> list:
    total_prompt = ""
    for message in conversation:
      if message["role"] == "system":
        total_prompt += f"""<|start_header_id|>system<|end_header_id|>

{ message['content']}<|eot_id|>"""

      if message["role"] == "user":
        total_prompt += f"""<|start_header_id|>user<|end_header_id|>

{ message['content'] }<|eot_id|>"""
      if message["role"] == "assistant":
        total_prompt += f"""<|start_header_id|>assistant<|end_header_id|>

{ message['content'] }<|eot_id|>"""

    return self.tokenize(total_prompt)

  def get_conversation_tokens(self, conversation: list[dict]) -> int:
    return len(self.apply_chat_template(conversation))

# kalle
# Copyright (C) 2024 Wayland Holdings, LLC

import os
import unittest
from kalle.lib.util.ConfigManager import ConfigManager
from kalle.lib.connectors.AnthropicConnector import AnthropicConnector
from kalle.lib.connectors.LLMConnector import LLMConnector
from kalle.lib.connectors.OllamaConnector import OllamaConnector
from kalle.lib.connectors.OpenAIConnector import OpenAIConnector
from kalle.lib.connectors.TabbyAPIConnector import TabbyAPIConnector
from kalle.lib.connectors.GroqConnector import GroqConnector

from kalle.lib.util.LLMConnectors import LLMConnectors
from kalle.domain.Profile import Profile, Connector


class TestLLMConnectors(unittest.TestCase):

  def setUp(self):
    appname = "kalle"
    appauthor = "fe2"
    self.fixtures_dir = os.path.join(os.path.dirname(__file__), "../../fixtures")
    self.config_file = os.path.join(self.fixtures_dir, "config.yml")
    os.environ["KALLE_CONFIG"] = self.config_file
    self.config = ConfigManager(
        appname, appauthor, conversation_key="default", base_file_dir=self.fixtures_dir, use_memory=False
    )
    self.llm_connectors = LLMConnectors(self.config)

  def test_init(self):
    self.assertEqual(self.llm_connectors.config, self.config)
    self.assertEqual(len(self.llm_connectors.connectors), 0)

  def test_get_connector_base(self):
    connector = self.llm_connectors.get_connector(Profile(key="base", connector=Connector(name="tabbyapi")), None)
    self.assertIsInstance(connector, LLMConnector)
    # only check this once
    self.assertEqual(len(self.llm_connectors.connectors), 1)

  def test_get_connectors(self):
    properties_to_test = [
        ("tabbyapi", TabbyAPIConnector),
        ("ollama", OllamaConnector),
        ("anthropic", AnthropicConnector),
        ("openai", OpenAIConnector),
        ("groq", GroqConnector),
    ]

    for name, connector_class in properties_to_test:
      with self.subTest(name=name, connector_class=connector_class):
        connector = self.llm_connectors.get_connector(Profile(key=name, connector=Connector(name=name)), None)
        self.assertIsInstance(connector, connector_class)

  def test_get_connector_cached(self):
    connector = self.llm_connectors.get_connector(Profile(key="base", connector=Connector(name="tabbyapi")), None)
    self.assertIsInstance(connector, LLMConnector)

    connector2 = self.llm_connectors.get_connector(Profile(key="base", connector=Connector(name="tabbyapi")), None)
    self.assertEqual(connector, connector2)


if __name__ == "__main__":
  unittest.main()

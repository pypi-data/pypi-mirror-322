# kalle
# Copyright (C) 2024 Wayland Holdings, LLC

import os
import unittest
from kalle.domain.ModelConfig import ModelConfig, ModelLocationType
from kalle.lib.util.ConfigManager import ConfigManager
from kalle.lib.util.ProfileManager import ProfileManager
from kalle.lib.connectors.LLMConnector import LLMConnector
from kalle.lib.connectors.TabbyAPIConnector import TabbyAPIConnector
from kalle.domain.Profile import Profile, Connector


class TestProfileManager(unittest.TestCase):

  def setUp(self):
    appname = "kalle"
    appauthor = "fe2"
    self.fixtures_dir = os.path.join(os.path.dirname(__file__), "../../fixtures")
    self.config_file = os.path.join(self.fixtures_dir, "config.yml")
    os.environ["KALLE_CONFIG"] = self.config_file
    self.config = ConfigManager(
        appname, appauthor, conversation_key="default", base_file_dir=self.fixtures_dir, use_memory=False
    )

  def test_init(self):
    profile_manager = ProfileManager(self.config, "base")
    self.assertEqual(profile_manager._config, self.config)
    self.assertIsInstance(profile_manager._profile, Profile)
    self.assertIsInstance(profile_manager._connector, LLMConnector)

  def test_init_with_model(self):
    profile_manager = ProfileManager(self.config, "base", "llama3_8b")
    self.assertEqual(profile_manager._config, self.config)
    self.assertIsInstance(profile_manager._profile, Profile)
    self.assertIsInstance(profile_manager._connector, LLMConnector)

  def test_profile(self):
    profile_manager = ProfileManager(self.config, "base")
    self.assertIsInstance(profile_manager.profile, Profile)

  def test_model(self):
    profile_manager = ProfileManager(self.config, "base")
    self.assertIsInstance(profile_manager.model, ModelConfig)

  def test_connector(self):
    profile_manager = ProfileManager(self.config, "base")
    self.assertIsInstance(profile_manager.connector, TabbyAPIConnector)


if __name__ == "__main__":
  unittest.main()

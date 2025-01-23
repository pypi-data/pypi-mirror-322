# kalle
# Copyright (C) 2024 Wayland Holdings, LLC

import unittest
import json
import os
import shutil
import tempfile
import time

from kalle.lib.util.ConfigManager import ConfigManager
from kalle.lib.util.ConversationTools import ConversationTools
from kalle.domain.Conversation import Conversation, ConversationMessage, ConversationMetadata


class TestConversationTools(unittest.TestCase):

  def setUp(self):
    self.temp_dir = tempfile.mkdtemp()
    self.maxDiff = 1000
    unittest.util._MAX_LENGTH = 2000

    appname = "kalle"
    appauthor = "fe2"
    self.fixtures_dir = os.path.join(os.path.dirname(__file__), "../../fixtures")
    self.config_file = os.path.join(self.fixtures_dir, "config.yml")
    os.environ["KALLE_CONFIG"] = self.config_file
    self.config = ConfigManager(
        appname, appauthor, conversation_key="default", base_file_dir=self.fixtures_dir, use_memory=False
    )
    self.config.yaml_config["data_dir"] = self.temp_dir
    self.conversation_tools = ConversationTools(self.config)

  def tearDown(self):
    shutil.rmtree(self.temp_dir)

  def test_init(self):
    self.assertEqual(self.conversation_tools.config, self.config)
    self.assertTrue(os.path.exists(self.config.conversation_dir))

  def test_set_conversation_key(self):
    conversation_key = "test_conversation_key"
    self.conversation_tools.set_conversation_key(conversation_key)
    self.assertEqual(self.conversation_tools.conversation_key, conversation_key)

  def test_list_conversations(self):
    # Create some test conversation files
    conversation_files = ["conversation_1.json", "conversation_2.json"]
    for file in conversation_files:
      with open(os.path.join(self.config.conversation_dir, file), "w") as f:
        json.dump({}, f)

    conversations = self.conversation_tools.list_conversations()
    self.assertEqual(conversations, ["1", "2"])

  def test_load_conversation(self):
    # Create a test conversation file
    conversation = {
        "metadata": {"version": "0.2"},
        "conversation": [
            {
                "timestamp": None,
                "system_prompt": None,
                "model": {},
                "uris": [],
                "piped": None,
                "role": "user",
                "content": "Hello",
            }
        ],
    }
    conversation_obj = Conversation(**conversation)
    self.config._conversation_key = "_test"
    with open(self.config.conversation_file, "w") as f:
      json.dump(conversation, f)

    loaded_conversation = self.conversation_tools.load_conversation()
    self.assertEqual(loaded_conversation, conversation_obj)

  def test_load_conversation_old(self):
    # Create a test conversation file
    conversation = [{"role": "user", "content": "This is a test"}]
    conversation_obj = Conversation(
        metadata=ConversationMetadata(version=0.2, system_prompt=None, profile=None),
        conversation=[
            ConversationMessage(
                timestamp=None,
                system_prompt=None,
                profile=None,
                role="user",
                piped_content=None,
                param_content=None,
                tool_prompt=None,
                tool_response=None,
                content="This is a test",
            )
        ],
    )
    self.config._conversation_key = "_test"
    with open(self.config.conversation_file, "w") as f:
      json.dump(conversation, f)

    loaded_conversation = self.conversation_tools.load_conversation()
    self.assertEqual(loaded_conversation, conversation_obj)

  def test_load_empty_conversation(self):
    # Create a test conversation file
    conversation_obj = Conversation()
    self.config._conversation_key = "_test"

    loaded_conversation = self.conversation_tools.load_conversation()
    self.assertEqual(loaded_conversation, conversation_obj)

  # early version of the newer format
  def test_load_conversation_missing_metadata(self):
    # Create a test conversation file
    conversation = {
        "conversation": [
            {
                "timestamp": None,
                "system_prompt": None,
                "model": {},
                "uris": [],
                "piped": None,
                "role": "user",
                "content": "Hello",
            }
        ],
    }
    conversation_obj = Conversation(**conversation)
    self.config._conversation_key = "_test"
    with open(self.config.conversation_file, "w") as f:
      json.dump(conversation, f)

    loaded_conversation = self.conversation_tools.load_conversation()
    self.assertEqual(loaded_conversation, conversation_obj)

  def test_persist_conversation(self):
    conversation = {
        "metadata": {"version": "0.2"},
        "conversation": [
            {
                "timestamp": None,
                "system_prompt": None,
                "model": {},
                "uris": [],
                "piped": None,
                "role": "user",
                "content": "Hello",
            }
        ],
    }
    conversation_obj = Conversation().model_validate_json(json.dumps(conversation))
    self.config._conversation_key = "_test"
    self.conversation_tools.persist_conversation(conversation_obj)

    with open(self.config.conversation_file, "r") as f:
      persisted_conversation = json.load(f)
      self.assertEqual(Conversation(**persisted_conversation), conversation_obj)

  def test_archive_conversation(self):
    # Create a test conversation file
    conversation = [{"message": "Hello"}]
    self.config._conversation_key = "_test"
    with open(self.config.conversation_file, "w") as f:
      json.dump(conversation, f)

    with open(f"{self.config.conversation_dir}/ollama_context_{self.config._conversation_key}.json", "w") as f:
      f.write("test")

    self.conversation_tools.archive_conversation()
    with open(self.config.conversation_file, "r") as f:
      file_contents = f.read()
    self.assertEqual(
        file_contents, '{"metadata":{"version":0.2,"system_prompt":null,"profile":null},"conversation":[]}'
    )

  def test_truncate_message_list(self):
    messages = [{"message": "Hello"}, {"message": "How are you?"}, {"message": "Goodbye"}]
    truncated_messages = self.conversation_tools.truncate_message_list(messages, 2)
    self.assertEqual(truncated_messages, [{"message": "How are you?"}, {"message": "Goodbye"}])

  def test_conversation_get_messages(self):
    conversation = {
        "metadata": {"version": "0.2"},
        "conversation": [
            {
                "timestamp": None,
                "system_prompt": None,
                "model": {},
                "uris": [],
                "piped": None,
                "role": "user",
                "content": "Hello",
            },
            {
                "timestamp": None,
                "system_prompt": None,
                "model": {},
                "uris": [],
                "piped": None,
                "role": "assistant",
                "content": "Hello back",
            },
        ],
    }
    conversation_obj = Conversation().model_validate_json(json.dumps(conversation))
    self.assertEqual(
        conversation_obj.get_messages(),
        [{"role": "user", "content": "Hello"}, {"role": "assistant", "content": "Hello back"}],
    )


if __name__ == "__main__":
  unittest.main()

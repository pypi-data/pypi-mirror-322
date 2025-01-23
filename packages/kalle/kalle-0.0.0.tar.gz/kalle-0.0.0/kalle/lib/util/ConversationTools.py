# kalle
# Copyright (C) 2024 Wayland Holdings, LLC

import datetime
import json
import os
import re

from kalle.domain.Conversation import Conversation, ConversationMetadata, ConversationMessage


class ConversationTools:

  def __init__(self, config):
    self.config = config
    if not os.path.exists(self.config.conversation_dir):
      os.makedirs(self.config.conversation_dir)

  @property
  def empty_conversation(self):
    return Conversation()

  @property
  def conversation_dir(self):
    return self.config.conversation_dir

  def set_conversation_key(self, conversation_key):
    self.conversation_key = conversation_key

  def list_conversations(self):
    directory = self.conversation_dir
    file_list = os.listdir(directory)
    conversations = [
        re.sub(r"^conversation_", "", re.sub(r"\..*", "", file)) for file in file_list if "conversation" in file
    ]
    conversations = sorted(list(set(conversations)))

    return conversations

  def load_conversation(self, path: str | None = None):
    conversation = self.empty_conversation

    # if not self.config.use_memory:
    # return conversation

    conversation_file = path or self.config.conversation_file
    if conversation_file is not None and os.path.exists(conversation_file):
      with open(conversation_file) as file:
        file_contents = file.read()
        if file_contents is not None and file_contents != "":
          file_contents_objects = json.loads(file_contents)
          if isinstance(file_contents_objects, list):
            # convert to new format
            new_file_contents = Conversation()
            for i in file_contents_objects:
              new_file_contents.conversation.append(
                  ConversationMessage(
                      role=i["role"],
                      content=i["content"],
                  )
              )
            file_contents = new_file_contents.model_dump_json()

          if "metadata" in file_contents_objects and isinstance(file_contents_objects["metadata"], dict):
            conversation_metadata = ConversationMetadata(version=file_contents_objects["metadata"]["version"])
            file_contents_objects["metadata"] = conversation_metadata

          conversation = Conversation().model_validate_json(file_contents)

    return conversation

  # persist conversation
  def persist_conversation(self, conversation, /, path: str | None = None):
    conversation_file = path or self.config.conversation_file

    if conversation_file is not None:
      with open(conversation_file, "w") as file:
        file.write(conversation.model_dump_json())

  # archive conversation
  def archive_conversation(self):
    if os.path.exists(self.config.conversation_file):
      now = datetime.datetime.now()
      stime = now.strftime("%Y-%m-%dT%H-%M-%S.%f")
      filename, _ = os.path.splitext(self.config.conversation_file)
      archive_file = f"{filename}.{stime}.json"
      os.rename(self.config.conversation_file, archive_file)

      # address ollama's persistence
      if os.path.exists(f"{self.config.conversation_dir}/ollama_context_{self.config.conversation_key}.json"):
        os.remove(f"{self.config.conversation_dir}/ollama_context_{self.config.conversation_key}.json")

      conversation = self.empty_conversation
      self.persist_conversation(conversation)

  # truncate to the last <count> messages
  def truncate_message_list(self, messages, count=10):
    return messages[-count:]

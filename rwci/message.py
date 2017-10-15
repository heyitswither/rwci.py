# -*- coding: utf-8 -*-

import datetime


class Message:
  def __init__(self, data):
    self.content = data.get('message')
    self.type = data.get('type')
    self.author = data.get('author')
    self.channel = data.get('channel')
    self.timestamp = datetime.datetime.now()

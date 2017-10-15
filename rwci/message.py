# -*- coding: utf-8 -*-

import datetime


class Message:
  def __init__(self, data):
    self.content = data['message']
    self.type = data['type']
    self.author = data['author']
    self.channel = data['channel']
    self.timestamp = datetime.datetime.now()

# -*- coding: utf-8 -*-


class User:
  def __init__(self, **kwargs):
    self.messages = []
    if not 'name' in kwargs:
      raise ValueError('A name must be specified')
    self.name = kwargs['name']

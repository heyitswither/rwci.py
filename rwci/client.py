# -*- coding: utf-8 -*-

import asyncio
import json
import logging
import sys

import websockets

from .errors import BadEventListener, BadLoginCredentials
from .message import Message
from .user import User

log = logging.getLogger("rwci")


class Client:
  def __init__(self, gateway_url):
    self.username = None
    self.password = None
    self.gateway_url = gateway_url
    self.ws = None
    self.funcs = {}
    self.user_list = []
    self.messages = []
    self.loop = asyncio.get_event_loop()

  async def connect(self):
    try:
      self.ws = await websockets.client.connect(self.gateway_url)
    except Exception as e:
      log.warn(e.__class__.__name__ + ": " + str(e))
      sys.exit()

  def event(self, coro):
    if not asyncio.iscoroutinefunction(coro):
      raise BadEventListener('Passed object must be awaitable')
    func_name = coro.__name__
    if not func_name.startswith("on_"):
      raise BadEventListener(
          "Event listeners should start with `on_` and then the payload type")

    self.funcs[func_name] = coro

    return coro

  async def get_latest_message(self):
    msg = await self.ws.recv()
    return msg

  async def _start(self):
    while True:
      t = await self.get_latest_message()
      if t is None:
        pass
      else:
        try:
          data = json.loads(t)
          await self.process_data(data)
        except BadLoiniCredentials:
          pass
        except Exception as e:
          log.warn(type(e).__name__ + ": " + str(e))
          log.warn("Non-JSON-serializable Object recieved from WeebSocket")
          log.warn(t)

  async def login(self, username, password):
    await self.connect()
    self.username = username
    self.password = password
    payload = {
        "type": "auth",
        "username": username,
        "password": password
    }
    await self.ws.send(json.dumps(payload))
    asyncio.ensure_future(self._start())
    while True:
      await asyncio.sleep(1)

  def run(self, username, password):
    try:
      self.loop.run_until_complete(self.login(username, password))
    except KeyboardInterrupt:
      self.loop.create_task(self.ws.close())
    finally:
      sys.exit()

  async def typing(self):
    payload = {
      "type": "typing"
    }
    await self.ws.send(json.dumps(payload))

  async def send(self, content):
    payload = {
        "type": "message",
        "message": content
    }
    await self.ws.send(json.dumps(payload))

  async def send_dm(self, content, recipient):
    payload = {
        "type": "direct_message",
        "message": content,
        "recipient": recipient
    }
    await self.ws.send(json.dumps(payload))

  async def wait_for_message(self):
    while True:
      t = await self.get_latest_message()
      if json.loads(t).get("type") == "message":
        if json.loads(t).get("author") != self.username:
          if self.funcs.get("on_message"):
            await self.funcs.get("on_message")(Message(json.loads(t)))
            self.messages.append(Message(json.loads(t)))
          return Message(json.loads(t))

  async def process_data(self, data):
    if data.get("type") == "auth":
      if data.get("success") == False:
        raise BadLoginCredentials("The login credentials entered were invalid")
      else:
        if self.funcs.get("on_ready") is not None:
          await self.funcs.get("on_ready")()

      if data.get("type") == "broadcast":
        if self.funcs.get("on_broadcast"):
          await self.funcs.get("on_broadcast")(data.get("message"))

    if data.get("type") == "message":
      if self.funcs.get("on_message"):
        await self.funcs.get("on_message")(Message(data))
        self.messages.append(Message(data))

    if data.get("type") == "direct_message":
      if self.funcs.get("on_direct_message"):
        await self.funcs.get("on_direct_message")(Message(data))
        self.messages.append(Message(data))

    if data.get("type") == "join":
      if self.funcs.get("on_join"):
        self.user_list.append(data.get("username"))
        await self.funcs.get("on_join")(data.get("username"))

    if data.get("type") == "quit":
      if self.funcs.get("on_quit"):
        self.user_list.remove(data.get("username"))
        await self.funcs.get("on_quit")(data.get("username"))

    if data.get("type") == "user_list":
      if self.funcs.get("on_user_list"):
        self.user_list = data.get("users")
        await self.funcs.get("on_user_list")(data.get("users"))

    if data.get("type") == "typing":
      if self.funcs.get("on_typing"):
        await self.funcs.get("on_typing")(data.get("username"))

    if self.funcs.get("on_raw_socket_recieve") is not None:
      await self.funcs.get("on_raw_socket_recieve")(data)

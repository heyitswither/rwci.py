#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""rwci/client.py
Copyright (c) 2017 Tucker Boniface
Licensed under MIT license."""

import asyncio
import json
import logging
import sys

import websockets

from .errors import BadEventListener, BadLoginCredentials
from .message import Message
# from .user import User

class Client:
    """Client object

       Contains all necessary methods for
       connecting to a websocket server,
       gathering incoming packets,
       and handling various client-related errors"""

    def __init__(self, gateway_url):
        self.username = None
        self.password = None
        self.gateway_url = gateway_url
        self.socket = None
        self.funcs = {}
        self.user_list = []
        self.messages = []
        self.loop = asyncio.get_event_loop()
        self.logger = logging.getLogger("rwci")

    async def connect(self):
        """Takes nothing
           Returns None

           Connects to the websocket server specified on instantiation"""
        try:
            self.socket = await websockets.client.connect(self.gateway_url)
        except websockets.exceptions.InvalidURI as exc:
            self.logger.warning("%s: %s", exc.__class__.__name__, str(exc))
            sys.exit(1)
        except websockets.exceptions.WebSocketProtocolError as exc:
            self.logger.warning("%s: %s", exc.__class__.__name__, str(exc))
            sys.exit(1)
        except websockets.exceptions.ConnectionClosed as exc:
            self.logger.warning("Connection closed: (code: %s) (reason: %s)", exc.code, exc.reason)
            sys.exit(1)

    def event(self, coro):
        """Takes coroutine
           Returns coroutine

           Handles event coroutines"""
        if not asyncio.iscoroutinefunction(coro):
            raise BadEventListener("Passed object must be awaitable")
        func_name = coro.__name__
        if not func_name.startswith("on_"):
            raise BadEventListener(
                "Event listeners should start with `on_` and then the payload type")

        self.funcs[func_name] = coro
        return coro

    async def get_latest_message(self):
        """Takes nothing
           Returns packet

           Responsible for receiving new packets from connected
           socket"""
        msg = await self.socket.recv()
        return msg

    async def _start(self):
        """Takes nothing
           Returns None

           Main packet gathering loop. Responsible for gathering
           packet and logging issues when loading the packet
           stream via JSON"""
        while True:
            latest_message = await self.get_latest_message()
            if latest_message is not None:
                try:
                    data = json.loads(latest_message)
                    await self.process_data(data)
                except BadLoginCredentials:
                    pass
                except json.decoder.JSONDecodeError as exc:
                    self.logger.warning("=========== [ Client / warninging ] ===========")
                    self.logger.warning("Non-JSON-serializable Object recieved from WeebSocket")
                    self.logger.warning("%s %s", type(exc).__name__, str(exc))
                    self.logger.warning(latest_message)
                    self.logger.warning("============================================")

    async def login(self, username, password):
        """Takes username and password
           Returns None

           Sends a login packet to the currently connected
           websocket server"""
        await self.connect()

        if len(username) > 32 or len(password) > 32:
            raise BadLoginCredentials(
                "Usernames/passwords must not exceed a length of 32 characters")

        username, password = username.replace("\n", ""), password.replace("\n", "")
        if "" in [username, password]:
            raise BadLoginCredentials(
                "Usernames/passwords must not be empty or consist of only spaces or newlines")

        self.username = username
        self.password = password
        payload = {
            "type": "auth",
            "username": username,
            "password": password
        }
        await self.socket.send(json.dumps(payload))
        asyncio.ensure_future(self._start())
        while True:
            await asyncio.sleep(1)

    def run(self, username, password):
        """Takes username and password
           Returns None

           Starts the event loops, logging into the server"""
        try:
            self.loop.run_until_complete(self.login(username, password))
        except KeyboardInterrupt:
            self.loop.create_task(self.socket.close())
        finally:
            sys.exit(0)

    async def typing(self):
        """Takes nothing
           Returns None

           Handles packets with type 'typing'
           """
        payload = {
            "type": "typing"
        }
        await self.socket.send(json.dumps(payload))

    async def send(self, content):
        """Takes content
           Returns None

           Sends a packet via socket to post a public message
           in connected websocket server"""
        payload = {
            "type": "message",
            "message": content
        }
        await self.socket.send(json.dumps(payload))

    async def send_dm(self, content, recipient):
        """Takes message content and intended deliveree
           Returns None

           Sends a packet via socket to directly message a user"""
        payload = {
            "type": "direct_message",
            "message": content,
            "recipient": recipient
        }
        await self.socket.send(json.dumps(payload))

    async def wait_for_message(self):
        """Takes None
           Returns Message

           Message loop. Gets messages from websocket and returns
           a Message object"""
        while True:
            latest_message = await self.get_latest_message()
            data = json.loads(latest_message)
            if data.get("type") == "message" and data.get("author") != self.username:
                if self.funcs.get("on_message"):
                    await self.funcs.get("on_message")(Message(json.loads(latest_message)))
                    self.messages.append(Message(json.loads(latest_message)))
                    return Message(json.loads(latest_message))

    async def process_data(self, data):
        """Takes data: JSON
           Returns None

           Handles packets of each type specified in the
           RWCI standard"""
        data_type = data.get("type")
        if data_type == "auth":
            if data.get("success") and self.funcs.get("on_ready") is not None:
                await self.funcs.get("on_ready")()
            else:
                raise BadLoginCredentials("The login credentials entered were invalid")

            if data_type == "broadcast" and self.funcs.get("on_broadcast"):
                await self.funcs.get("on_broadcast")(data.get("message"))

        if data_type == "message" and self.funcs.get("on_message"):
            await self.funcs.get("on_message")(Message(data))
            self.messages.append(Message(data))

        if data_type == "direct_message" and self.funcs.get("on_direct_message"):
            await self.funcs.get("on_direct_message")(Message(data))
            self.messages.append(Message(data))

        if data_type == "join" and self.funcs.get("on_join"):
            self.user_list.append(data.get("username"))
            await self.funcs.get("on_join")(data.get("username"))

        if data_type == "quit" and self.funcs.get("on_quit"):
            self.user_list.remove(data.get("username"))
            await self.funcs.get("on_quit")(data.get("username"))

        if data_type == "user_list" and self.funcs.get("on_user_list"):
            self.user_list = data.get("users")
            await self.funcs.get("on_user_list")(data.get("users"))

        if data_type == "typing" and self.funcs.get("on_typing"):
            await self.funcs.get("on_typing")(data.get("username"))

        if self.funcs.get("on_raw_socket_recieve") is not None:
            await self.funcs.get("on_raw_socket_recieve")(data)

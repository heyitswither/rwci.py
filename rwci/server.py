import websockets
import asyncio
import json
import sys
import bcrypt
import logger

import .errors

class Server:
    def __init__(self, host, port, ssl=None):
        self.users = {}
        self.ssl = ssl # ssl context provided by main
        self.ws = None
        self.channels = set() # TODO: channel object
        self.default_channel = {}
        self.groups = set() # TODO: group object
        self.funcs = {}
        self.loop = asyncio.get_event_loop()
        self.logger = logging.getLogger("rwci")

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

# Will be similar to rwci.Client
# Main adds event listeners + provided ssl
# lots to do

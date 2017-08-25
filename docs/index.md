# API Reference

The following section outlines the API of rwci.py.

> **Note:** This module uses the Python logging module to log diagnostic and errors in an output independent way. If the logging module is not configured, these logs will not be output anywhere. See [Setting Up Logging](http://rwcipy.rtfd.io/en/latest/logging/) for more information on how to set up and use the logging module with rwci.py.

## Client

`class rwci.Client(*, **options)`

Represents a client connection that connects to an RWCI compatible websocket server. This class is used to interact with the WebSocket.

Parameters:

- **gateway_url** *(Optional[str])* - The websocket server to use in communications. This defaults to 'ws://a-sketchy.site:5000'

Attributes:

`gateway_url` `str` - The websocket server that the client connects to

`ws` `(Optional[websockets.client.WebSocketClientProtocol])` - The websocket gateway the client is currently connected to. Could be None if not connected to the gateway.

`messages` `list` - A list of `rwci.Message` objects that the client has recieved

`loop` `_UnixSelectorEventLoop` - The [event loop](https://docs.python.org/3/library/asyncio-eventloops.html) that the client uses for websocket operations.

Methods:

`run(username, password)`

Creates a loop, then calls login() inside the loop

```py
client.run('username', 'password')
```

This function is blocking, all declarations should be made before this function call.

`send(content)`

This function is a [coroutine](https://docs.python.org/3/library/asyncio-task.html#coroutine).

Sends a message to the server with the given `content`

```py
await client.send('Hello world!')
```

`send_dm(content, recipient)`

This function is a [coroutine](https://docs.python.org/3/library/asyncio-task.html#coroutine).

Sends a message to the given user with the given `content`

```py
await client.send_dm('Hello!', 'joseph')
```

`connect()`

This function is a [coroutine](https://docs.python.org/3/library/asyncio-task.html#coroutine).

Creates a connection to the websocket server.

This method usually isn't called by the end user.

`login(username, password)`

This function is a [coroutine](https://docs.python.org/3/library/asyncio-task.html#coroutine).

Logs in the client with the specified credentials.

This method usually isn't called by the end user.

`get_latest_message()`

This function is a [coroutine](https://docs.python.org/3/library/asyncio-task.html#coroutine).

Returns a `str` data packet from the server.

This method usually isn't called by the end user.

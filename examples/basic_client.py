import rwci

client = rwci.Client(gateway_url="your gateway url")

@client.event
async def on_ready():
  print("Client online")
  await client.send("Hello, world!")

@client.event
async def on_message(message):
  print("{0.author}: {0.content}".format(message))

@client.event
async def on_user_list(users):
  print("Online users")
  for user in users:
    print("    - "+user)

@client.event
async def on_join(username):
  print(username+" joined us!")

@client.event
async def on_quit(username):
  print(username+" left us! :(")

@client.event
async def on_broadcast(broadcast):
  print("Server broadcast: "+broadcast)

@client.event
async def on_typing(username):
  print(f"{username} is typing")

client.run("username","password")

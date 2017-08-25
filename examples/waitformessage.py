import rwci

client = rwci.Client(gateway_url="your gateway")

@client.event
async def on_message(message):
    if message.content == "!say":
        await client.send("What should I say?")
        res = await client.wait_for_message()
        await client.send(res.content)
        
client.run("username","password")

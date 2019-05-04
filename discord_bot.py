import discord

client = discord.Client()

@client.event
async def on_ready():
    print("Deployment Successful")
    await client.change_presence(activity=discord.Game(name="python3.6"))

@client.event
async def on_message(message):
    if message.content == "!test":
    	channel = message.channel
    	await channel.send("Test Successful")
        #await client.send(message.channel, "Test Successful")

tokendat = open("token.dat", "r")
client.run(tokendat.read().strip())
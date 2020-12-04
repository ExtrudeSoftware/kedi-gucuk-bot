from utils import *

client = commands.Bot(command_prefix=prefix)

@client.event
async def on_ready():
    print("Bot: %s\nBotID: %s\nBot hazır." % (str(botName), str(botID)))

@client.event
async def on_message(message):
    if message.author.id == botID:
        return
    if message.content.strip() == "selam":
        await message.channel.send("selam, " + message.author.mention)

    else:
        await client.process_commands(message) # komutu çalıştır

@client.command()
async def ping(ctx): # async def komut adı parametreler
    await ctx.send("Pong! Gecikme: %s" % str(round(client.latency, 1)))




client.run(token)
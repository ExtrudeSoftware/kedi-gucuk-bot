from utils import *

client = commands.Bot(command_prefix=prefix)

@client.event
async def on_ready():
    for file in os.listdir(os.path.join(os.path.dirname(__file__), "cogs")):
        if file.endswith(".py"):
            try:
                client.load_extension(f"cogs.{file.split('.')[0]}")
            except:
                print(f"Komut Yüklenemedi: {file.split('.')[0]}")
            else:
                print(f"Komut Yüklendi: {file.split('.')[0]}")

    print("\n\nBot: %s\nBotID: %s\nBot hazır." % (str(botName), str(botID)))

@client.event
async def on_message(message):
    if message.author.bot:
        return
    else:
        await client.process_commands(message) # komutu çalıştır

@client.event
async def on_member_join(member):
    channel = client.get_channel("780384785544904754")
    await channel.send("biri geldi mlpy ")
    print(f"{member} sunucuya katıldı.")


@client.event
async def on_member_remove(member):
    print(f"{member} sunucudan ayrıldı.")

@client.command()
async def ping(ctx): # async def komut adı parametreler
    await ctx.send("Gecikme: %s" % str(round(client.latency, 1)))


client.run(token)
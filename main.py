from utils import *

intents = discord.Intents(messages=True, guilds=True, members=True)
client = commands.Bot(command_prefix=prefix, intents=intents, case_insensitive=True)
client.remove_command('help')

async def isAuthor(ctx):
    if ctx.author.id in author:
        return True
    else:
        await ctx.send("Bu komutu kullanmak için yetkiniz bulunmamaktadır.")
        
 
@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle, activity=discord.Game(name="k!yardım"))

    for file in os.listdir(os.path.join(os.path.dirname(__file__), "cogs")):
        if file.endswith(".py"):
            try:
                client.load_extension(f"cogs.{file.split('.')[0]}")
            except Exception as e:
                print(f"[WARN] Cog yüklenemedi: {file.split('.')[0]}")
                print(f"[ERROR] {e}")
            else:
                print(f"[INFO] Cog yüklendi: {file.split('.')[0]}")

    print("\n\nBot: %s\nBotID: %s\nBot hazır.\n\n" % (str(botName), str(botID)))


@client.event
async def on_message(message):
    if message.author.bot:
        return
    else:
        await client.process_commands(message) # komutu çalıştı

@client.event
async def on_command_error(ctx, error): # Komut çalışırken hata alınırsa
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Yeterli yetkin bulunmamakta.")
    
    try:
        print(f"[WARN] {ctx.command.name} komutu {ctx.author} tarafından çalıştırılırken bir hata meydana geldi:\n{error}")
    except:
        print("[WARN] Bilinmeyen bir komut alındı.")
        
@client.event
async def on_command_completion(ctx): # Komut sorunsuz çalışırsa
	print(f"[INFO] {ctx.command.name} komutu {ctx.author} tarafından başarıyla çalıştırıldı.")


@client.event
async def on_member_join(member):
    print(f"{member}, katıldı.")

@client.event
async def on_member_remove(member):
    print(f"{member}, ayrıldı." )

@client.command()
@commands.check(isAuthor)
async def loadcog(ctx, cogname):
    try:
        client.load_extension(f"cogs.{cogname}")
    except Exception as e:
        print(f"[WARN] Kullanıcı girişi ile cog yüklenemedi: {cogname}")
        print(f"[ERROR] {e}")
        await ctx.send(f"{cogname} yüklenirken bir hata oluştu.")
    else:
        print(f"[INFO] Kullanıcı girişi ile yüklenen cog: {cogname}")
        await ctx.send(f"{cogname} başarıyla yüklendi.")

@client.command()
@commands.check(isAuthor)
async def delcog(ctx, cogname):
    try:
        client.unload_extension(f"cogs.{cogname}")
    except Exception as e:
        print(f"[WARN] Kullanıcı girişi ile cog silinemedi: {cogname}")
        print(f"[ERROR] {e}")
        await ctx.send(f"{cogname} kaldırılırken bir hata oluştu.")
    else:
        print(f"[INFO] Kullanıcı girişi ile silinen cog: {cogname}")
        await ctx.send(f"{cogname} başarıyla kaldırıldı.")

@client.command()
@commands.check(isAuthor)
async def delallcogs(ctx):
    basari = []
    fail = []
    
    for file in os.listdir(os.path.join(os.path.dirname(__file__), "cogs")):
        if file.endswith(".py"):
            try:
                client.unload_extension(f"cogs.{file.split('.')[0]}")
            except Exception as e:
                print(f"[WARN] Kullanıcı girişi ile cog silinemedi: {file.split('.')[0]}")
                print(f"[ERROR] {e}")
                fail.append(file.split(".")[0])
            else:
                print(f"[INFO] Kullanıcı girişi ile silinen cog: {file.split('.')[0]}")
                basari.append(file.split(".")[0])

    basari = ",".join(basari)
    fail = ",".join(fail)

    await ctx.send(f"Silinen coglar: {basari}\nSilinemeyen coglar: {fail}")       
    
@client.command()
@commands.check(isAuthor)
async def loadallcogs(ctx):
    basari = []
    fail = []
    
    for file in os.listdir(os.path.join(os.path.dirname(__file__), "cogs")):
        if file.endswith(".py"):
            try:
                client.load_extension(f"cogs.{file.split('.')[0]}")
            except Exception as e:
                print(f"[WARN] Kullanıcı girişi ile cog yüklenemedi: {file.split('.')[0]}")
                print(f"[ERROR] {e}")
                fail.append(file.split(".")[0])
            else:
                print(f"[INFO] Kullanıcı girişi ile yüklenen cog: {file.split('.')[0]}")
                basari.append(file.split(".")[0])

    basari = ",".join(basari)
    fail = ",".join(fail)

    await ctx.send(f"Yüklenen coglar: {basari}\nYüklenemeyen coglar: {fail}")


@client.command()
async def ping(ctx):
    await ctx.send("Gecikme: %sms" % str(round(client.latency, 1)))

@client.command(aliases=["help", "y", "feedback", "geribildirim", "şikayet", "komutlar", "commands", "h"])
async def yardım(ctx):
    embed=discord.Embed(title="Yardım", color=0xdbf708)
    embed.set_thumbnail(url="https://camo.githubusercontent.com/9c71d96ccd0bc414e3caf4bf2a5ce273f53e796286b60fbdbecc13f7fed79448/68747470733a2f2f63646e2e646973636f72646170702e636f6d2f6174746163686d656e74732f3636303830373139313033363535393339322f3738353831393335393132383937373432392f756e6b6e6f776e2e706e67")
    embed.add_field(name="Hata ve geri bildirim için", value="https://github.com/gucukyazilim/kedi-gucuk-bot-wiki/issues", inline=False)
    embed.add_field(name="Kullanım kılavuzu için", value="https://github.com/gucukyazilim/kedi-gucuk-bot-wiki/wiki", inline=False)
    await ctx.send(embed=embed)


client.run(token)
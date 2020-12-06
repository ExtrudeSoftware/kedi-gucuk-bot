from utils import *

client = commands.Bot(command_prefix=prefix)

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
    try:
        print(f"[WARN] {ctx.command.name} komutu {ctx.author} tarafından çalıştırılırken bir hata meydana geldi:\n{error}")
    except:
        print("[WARN] Bilinmeyen bir komut alındı.")
        
@client.event
async def on_command_completion(ctx): # Komut sorunsuz çalışırsa
	print(f"[INFO] {ctx.command.name} komutu {ctx.author} tarafından başarıyla çalıştırıldı.")


@client.event
async def on_member_join(member):
    print("biri geldi ml")
    

@client.command()
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

    

client.run(token)
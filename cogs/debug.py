import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import *

async def isAuthor(ctx):
    if ctx.author.id in author:
        return True
    else:
        await ctx.send("Bu komutu kullanmak için yetkiniz bulunmamaktadır.")

class Debug(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.check(isAuthor)
    async def reboot(self, ctx):
        await ctx.send("Bot yeniden başlatılıyor...")
        os.system(f"@cls && @python {mainPath}")
        
    @commands.command()
    @commands.check(isAuthor)
    async def shutdown(self, ctx):
        await ctx.send("Bot kapatılıyor...")
        sys.exit(f"{ctx.author} adlı kullanıcının girişi ile bot kapatılmıştır.")

    @commands.command()
    @commands.check(isAuthor)
    async def isAuthor(self, ctx, member:discord.Member=None):
        if not member:
            o = ctx.author.id in author
            await ctx.send(o)
        else:
            o = member.id in author
            await ctx.send(o)

def setup(client):
    client.add_cog(Debug(client))

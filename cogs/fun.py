import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import *

class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["söyle", "print", "say"])
    async def yazdır(self, ctx, *, mesaj=None):
        if not mesaj:
            await ctx.send("Yazdırılacak mesajı belirlemelisin.")
        else:
            await ctx.send(mesaj)
    
    @commands.command(aliases=["printndel", "sayndel"])
    async def yazdırsil(self, ctx, *, mesaj=None):
        if not mesaj:
            await ctx.send("Yazdırılacak mesajı belirlemelisin.")
        else:
            await ctx.message.delete()
            await ctx.send(mesaj)

    @commands.command(aliases=["kura", "choice", "rastgele"])
    async def çekiliş(self, ctx, *msg):
        if len(msg) <= 1: 
            await ctx.send("En az 2 parametre girmeniz gerekmektedir.")
            return
        await ctx.send(ran.choice(msg))

def setup(client):
    client.add_cog(Fun(client))

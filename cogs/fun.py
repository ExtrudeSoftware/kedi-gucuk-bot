import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import *

class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def yazdır(self, ctx, *, mesaj):
        msg = mesaj.split(" ")
        for i in msg:
            if i == "-i" or i == "--ignore": # ignore the syntax rules
                mesaj = mesaj.replace("-i" if i == "-i" else "--ignore", "")
                break 

            if i == "-d" or i == "--del": # delete the authors' message after using this command
                await ctx.message.delete()
                mesaj = mesaj.replace("-d" if i == "-d" else "--del" , "")
                
        await ctx.send(mesaj)
    
    @commands.command()
    async def çekiliş(self, ctx, *msg):
        if len(msg) <= 1: 
            await ctx.send("En az 2 parametre girmeniz gerekmektedir.")
            return
        await ctx.send(ran.choice(msg))

def setup(client):
    client.add_cog(Fun(client))

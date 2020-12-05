import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import *


class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command(pass_context=True, aliases=["purge","clear"])
    @commands.has_permissions(manage_messages=True)
    @commands.guild_only()
    async def temizle(self, ctx, amount=""):
        if not amount:
            await ctx.send("Lütfen silinecek mesaj miktarını belirleyiniz.")
            return
        try:
            amount = int(amount)
        except:
            await ctx.send("Lütfen sadece bir sayı belirleyiniz.")
            return

        if amount <= 0:
            await ctx.send("Lütfen 0'dan büyük bir sayı giriniz.")
            return
        
        await ctx.channel.purge(limit=amount)

    @temizle.error
    async def temizle_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Yeterli yetkin yok.")
    



def setup(client):
    client.add_cog(Moderation(client))

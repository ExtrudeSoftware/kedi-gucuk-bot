import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import *


class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True, aliases=["engel"])
    @commands.has_permissions(ban_members=True)
    @commands.guild_only()
    async def ban(self,ctx, member:discord.Member=None, *, reason="Sebep verilmemiş"):
        if not member:
            await ctx.send("Banlamak için üye belirlemelisiniz.")
        else:
            await member.ban(reason=reason)

    @commands.command(pass_context=True, aliases=["at"])
    @commands.has_permissions(kick_members=True)
    @commands.guild_only()
    async def kick(self, ctx, member:discord.Member=None, *, reason="Sebep verilmemiş"):
        if not member:
            await ctx.send("Kick için üye belirlemelisiniz.")
        else:
            await member.kick(reason=reason)
    
    @commands.command(pass_context=True, aliases=["bankaldır", "engelkaldır"])
    @commands.has_permissions(ban_members=True)
    @commands.guild_only()
    async def unban(self, ctx, *, member=None):
        if not member:
            await ctx.send("Banını kaldırmak istediğiniz kullanıcıyı belirtmelisiniz.")
        else:
            banned_users = await ctx.guild.bans()
            
            member_name, member_discriminator = member.split('#')
            for ban_entry in banned_users:
                user = ban_entry.user
                
                if (user.name, user.discriminator) == (member_name, member_discriminator):
                    await ctx.guild.unban(user)    


    @commands.command(pass_context=True, aliases=["purge","clear"])
    @commands.has_permissions(manage_messages=True)
    @commands.guild_only()
    async def temizle(self, ctx, amount=""):
        if not amount:
            return await ctx.send("Lütfen silinecek mesaj miktarını belirleyiniz.")
        try:
            amount = int(amount)
        except:
            return await ctx.send("Lütfen sadece bir sayı belirleyiniz.")
        if amount <= 0:
            return await ctx.send("Lütfen 0'dan büyük bir sayı giriniz.")     

        await ctx.channel.purge(limit=amount)
        await ctx.send(f":white_check_mark: {amount} mesaj {ctx.author.mention} tarafından silindi.", delete_after=3)

    @commands.command(pass_context=True, aliases=["purgeu","purgeuser"])
    @commands.has_permissions(manage_messages=True)
    @commands.guild_only()    
    async def ktemizle(self, ctx, member:discord.Member, limit:int=None):
        if not member:
            return await ctx.send("Üye belirlemelisin.")

        if not limit:
            return await ctx.send("Limit belirlemelisin.")

        msg = []
        async for m in ctx.channel.history():
            if len(msg) == limit:
                break
            if m.author == member:
                msg.append(m)

        await ctx.channel.delete_messages(msg)
        await ctx.send(f"{member.mention} kullanıcısının {limit} mesajı {ctx.author.mention} tarafından silindi.", delete_after=3)

def setup(client):
    client.add_cog(Moderation(client))

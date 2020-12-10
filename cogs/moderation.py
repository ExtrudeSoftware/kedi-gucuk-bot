import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import *


class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command(pass_context=True, aliases=["engel"])
    @commands.has_permissions(ban_members=True)
    @commands.guild_only()
    async def ban(self,ctx, member:discord.Member=None, *, reason="sebep verilmemiş"):
        if not member:
            return await ctx.send("Banlamak için üye belirlemelisiniz.")

        if member.guild_permissions.administrator:
            return await ctx.send("Yönetici bir kullanıcıyı banlayamazsın.")
        
        try:
            await member.ban(reason=reason)
        except:
            await ctx.message.add_reaction(FAIL_EMOJI)
        else:
            await ctx.message.add_reaction(OK_EMOJI)

    @commands.command(pass_context=True, aliases=["at"])
    @commands.has_permissions(kick_members=True)
    @commands.guild_only()
    async def kick(self, ctx, member:discord.Member=None, *, reason="Sebep verilmemiş"):
        if not member:
            return await ctx.send("Kick için üye belirlemelisiniz.")
        
        if member.guild_permissions.administrator:
            return await ctx.send("Yönetici bir kullanıcıyı sunucudan atamazsın.")

        try:
            await member.kick(reason=reason)
        except:
            await ctx.message.add_reaction(FAIL_EMOJI)
        else:
            await ctx.message.add_reaction(OK_EMOJI)

    @commands.command(pass_context=True, aliases=["bankaldır", "engelkaldır"])
    @commands.has_permissions(ban_members=True)
    @commands.guild_only()
    async def unban(self, ctx, member=None):
        if not member:
            await ctx.send("Banını kaldırmak istediğiniz kullanıcıyı belirtmelisiniz.")
        else:
            try:
                banned_users = await ctx.guild.bans()
                
                member_name, member_discriminator = member.split('#')
                
                for ban_entry in banned_users:
                    user = ban_entry.user
                        
                    if (user.name, user.discriminator) == (member_name, member_discriminator):
                        await ctx.guild.unban(user)
            except ValueError:
                try:
                    await ctx.guild.unban(await self.client.fetch_user(int(member)))
                except:
                    await ctx.send("Geçersiz kullanıcı.")
                    await ctx.message.add_reaction(FAIL_EMOJI)
                else:
                    await ctx.message.add_reaction(OK_EMOJI)

            else:
                await ctx.message.add_reaction(OK_EMOJI)
            


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

        try:
            await ctx.channel.purge(limit=amount)
        except:
            await ctx.message.add_reaction(FAIL_EMOJI)
        else:
            await ctx.message.add_reaction(OK_EMOJI)
            await ctx.send(f":white_check_mark: {amount} mesaj {ctx.author.mention} tarafından silindi.", delete_after=3)

    @commands.command(pass_context=True, aliases=["purgeu","purgeuser"])
    @commands.has_permissions(manage_messages=True)
    @commands.guild_only()
    async def ktemizle(self, ctx, member:discord.Member=None, limit:int=None):
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


    @commands.command(pass_context=True, aliases=["sustur"])
    @commands.has_permissions(manage_roles=True)
    @commands.guild_only()
    async def mute(self, ctx, member:discord.Member=None, *, reason="sebep belirtilmemiş"):
        if not member:
            return await ctx.send("Mute için kullanıcı belirleyiniz.")
        
        if member.bot:
            return await ctx.send("Bot kullanıcıları muteleyemezsin.")
        
        if member.guild_permissions.administrator:
            return await ctx.send("Yönetici bir kullanıcıyı muteleyemezsin.")

        if discord.utils.get(member.roles, name="GucukMute"):
            return await ctx.send("Bu kullanıcı zaten muteli.")

        ###########
        
        if not discord.utils.get(ctx.guild.roles, name="GucukMute"):   
            perms = discord.Permissions(send_messages=False, read_messages=True)
            role = await ctx.guild.create_role(name="GucukMute", permissions=perms) 

        else:
            role = discord.utils.get(ctx.guild.roles, name="GucukMute")        

        for channel in self.client.get_guild(ctx.guild.id).channels: await channel.set_permissions(role, send_messages=False)
        await member.add_roles(role)
        
        await ctx.send(f"{member.mention} kullanıcısı {ctx.author.mention} tarafından \'{reason}\' sebebiyle susturulmuştur.")
        

    @commands.command(pass_context=True, aliases=["timemute","zsustur"])
    @commands.has_permissions(manage_roles=True)
    @commands.guild_only()
    async def tmute(self, ctx, member:discord.Member=None, *, args):
        args = args.split(" ")
        try:
            minutes = int(args[0])
        except: return await ctx.send("Sadece sayı giriniz.")

        if not member:
            return await ctx.send("Time mute için kullanıcı belirleyiniz.")
        
        if member.bot:
            return await ctx.send("Bot kullanıcıları muteleyemezsin.")
        
        if member.guild_permissions.administrator:
            return await ctx.send("Yönetici bir kullanıcıyı muteleyemezsin.")

        if discord.utils.get(member.roles, name="GucukMute"):
            return await ctx.send("Bu kullanıcı zaten muteli.")

        if minutes <= 0:
            return await ctx.send("Dakika, 0 ya da 0\'dan küçük olamaz.")
        
        if not args[1:]:
            reason = "sebep verilmemiş"
        else:
            reason = " ".join(args[1:])

        ##############################

        if not discord.utils.get(ctx.guild.roles, name="GucukMute"):   
            perms = discord.Permissions(send_messages=False, read_messages=True)
            role = await ctx.guild.create_role(name="GucukMute", permissions=perms) 

        else:
            role = discord.utils.get(ctx.guild.roles, name="GucukMute")

        for channel in self.client.get_guild(ctx.guild.id).channels: await channel.set_permissions(role, send_messages=False)
        await member.add_roles(role)
        
        await ctx.send(f"{member.mention} kullanıcısı {ctx.author.mention} tarafından \'{reason}\' sebebiyle {minutes} dakika boyunca susturulmuştur.")

        await asyncio.sleep(minutes * 60)
        await member.remove_roles(role)
        
        

    @commands.command(pass_context=True, aliases=["konuş","susturkaldır"])
    @commands.has_permissions(manage_roles=True)
    @commands.guild_only()
    async def unmute(self, ctx, member:discord.Member=None):
        if not member:
            return await ctx.send("Unmute için kullanıcı belirleyiniz.")

        if not discord.utils.get(member.roles, name="GucukMute"):
            return await ctx.send("Kullanıcı zaten muteli değil.")

        role = discord.utils.get(ctx.guild.roles, name="GucukMute")
        await member.remove_roles(role)

        await ctx.send(f"{member.mention} kullanısının mute cezası {ctx.author.mention} tarafından kaldırılmıştır.")
  
    
def setup(client):
    client.add_cog(Moderation(client))

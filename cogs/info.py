import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import *


class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["pfp", "profilf","kullanıcıf","avatar"])
    async def pp(self, ctx, member:discord.Member=None):
        if not member:
            member = ctx.author
            
        embed=discord.Embed()
        embed=discord.Embed(title=f"{member} adlı kullanıcının profil resmi")
        embed.set_image(url=member.avatar_url)
        await ctx.send(embed=embed)


    @commands.command(aliases=["kb","kullanıcıbilgisi","userinfo"])
    async def kullanıcıbilgi(self, ctx, member:discord.Member=None):
        if not member:
            member = ctx.author
            
        roles = [role for role in member.roles]

        embed = discord.Embed(colour=member.color,timestamp=ctx.message.created_at)

        embed.set_author(name=f"Kullanıcı Bilgisi - {member}")
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=f"{ctx.author} tarfından istendi",icon_url=ctx.author.avatar_url)

        embed.add_field(name="ID:",value=member.id)
        embed.add_field(name="Sunucudaki adı:",value=member.display_name)

        embed.add_field(name="Hesabın oluşturulma zamanı:",value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
        embed.add_field(name="Sunucuya katılma zamanı:",value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))

        embed.add_field(name=f"Rolleri({len(roles)}):",value=" ".join([role.mention for role in roles]))
        embed.add_field(name="En yüksek rolü:",value=member.top_role.mention)

        embed.add_field(name="Bot ?",value=member.bot)
        await ctx.send(embed=embed)
    
    @commands.command(aliases=["si","gi","servericon","guildicon"])
    async def sunucuikonu(self, ctx):
        embed=discord.Embed()
        embed = discord.Embed(title=f"{ctx.author.guild}, sunucusunun ikonu.")
        embed.set_image(url=ctx.guild.icon_url)

        await ctx.send(embed=embed)
        
    @commands.command(aliases=["sunucubilgi","svinfo","guildinfo"])
    async def serverinfo(self, ctx):
        name = str(ctx.guild.name)
        description = str(ctx.guild.description)

        owner = str(ctx.guild.owner)
        gid = str(ctx.guild.id)
        region = str(ctx.guild.region)
        memberCount = str(ctx.guild.member_count)

        icon = str(ctx.guild.icon_url)
        
        embed = discord.Embed(
            title=name + " Sunucu bilgisi",
            description="Açıklama: "+description,
            color=discord.Color.blue()
            )
        embed.set_thumbnail(url=icon)
        embed.add_field(name="Sahip", value=owner, inline=True)
        embed.add_field(name="Sunucu ID", value=gid, inline=True)
        embed.add_field(name="Bölge", value=region, inline=True)
        embed.add_field(name="Üye Sayısı", value=memberCount, inline=True)

        await ctx.send(embed=embed)
    
    @commands.command(aliases=["guildroles", "gr", "guildr","serverroles","roles","sr"])
    async def roller(self, ctx):
        roles = []

        for role in ctx.guild.roles:
            
            if str(role) == "@everyone":
                roles.append("@everyone")
            else:
                role_mention = ("<@&" + (str(role.id)) + ">")
                roles.append( role_mention )
            
        roles = "\n".join(roles)

        embed=discord.Embed(title=f"{ctx.guild.name} sunucusunun rolleri", color=0xe10e0e)
        embed.add_field(name="Roller", value=f"{roles}", inline=False)

        try:
            await ctx.send(embed=embed)
        except:
            roles = []
            for role in ctx.guild.roles: roles.append( "@" + (str(role)).replace("@","") )
            roles = "\n".join(roles)
            await ctx.send("Mesaj 2000 karakterden fazla, Pastebin\'e yükledim: " + pastebinpost("Kedi Gucuk", "text", roles))

def setup(client):
    client.add_cog(Moderation(client))

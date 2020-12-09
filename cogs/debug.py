import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import *

def insert_returns(body):
    # insert return stmt if the last expression is a expression statement
    if isinstance(body[-1], ast.Expr):
        body[-1] = ast.Return(body[-1].value)
        ast.fix_missing_locations(body[-1])

    # for if statements, we insert returns into the body and the orelse
    if isinstance(body[-1], ast.If):
        insert_returns(body[-1].body)
        insert_returns(body[-1].orelse)

    # for with blocks, again we insert returns into the body
    if isinstance(body[-1], ast.With):
        insert_returns(body[-1].body)


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
    
    @commands.command()
    async def uptime(self, ctx):
        end_time = time.time()
        zaman = int(end_time - start_time) # geçen zaman
        
        saniye = zaman % 60
        dakika = zaman // 60
        saat = zaman // 3600
        
        await ctx.send(f"Bot, {saat} saat, {dakika} dakika, {saniye} saniyedir açık.") 


    @commands.command(name="eval", pass_context=True)
    @commands.check(lambda ctx: ctx.author.id in author)
    async def _eval(self, ctx, *, cmd):
        fn_name = "_eval_expr"

        cmd = cmd.strip("` ")

        # add a layer of indentation
        cmd = "\n".join(f"    {i}" for i in cmd.splitlines())

        # wrap in async def body
        body = f"async def {fn_name}():\n{cmd}"

        parsed = ast.parse(body)
        body = parsed.body[0].body

        insert_returns(body)

        env = {
            'client': ctx.bot,
            'discord': discord,
            'commands': commands,
            'ctx': ctx,
            '__import__': __import__
        }

        exec(compile(parsed, filename="<ast>", mode="exec"), env)

        result = (await eval(f"{fn_name}()", env))
        #await ctx.send(result)

        
        
def setup(client):
    client.add_cog(Debug(client))

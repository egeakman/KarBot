import inspect
import io
import textwrap
import traceback
from contextlib import redirect_stdout
import datetime
from speedtest import Speedtest
from psutil import virtual_memory, cpu_percent, cpu_freq
from subprocess import run, DEVNULL
import discord
from discord.ext import commands

class Debug(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(error.original)

    @commands.Cog.listener()
    async def on_ready(self):
        print("Debug is ready.")

    def this_should_be_me(ctx):
        return ctx.author.id == 358689309215293443

    @commands.command(name='speedtest')
    async def speed_test(self, ctx):
        """Speedtest"""
        async with ctx.typing():
            s = Speedtest()
            s.get_best_server()
            s.download()
            s.upload()
            s = s.results.dict()

            em = discord.Embed(title="Speedtest Results", color=0x00CC99)
            em.add_field(name=':ping_pong: Ping', value=f"**`{round(s['ping'], 1)}ms`**")
            em.add_field(name=':arrow_down: Download', value=f"**`{round(s['download']/10**6, 1)} Mbits/s`**")
            em.add_field(name=':arrow_up: Upload', value=f"**`{round(s['upload']/10**6, 1)} Mbits/s`**")
            em.add_field(name=':satellite_orbital: Server', value=f"**`{s['server']['sponsor']}, {s['server']['name']}, {s['server']['country']}`**")
            em.set_thumbnail(url="https://i.ibb.co/JK1z40M/a51b83cb114408930389ecd8f5412a9d.png")

            try:
                await ctx.send(embed=em)
            except Exception:
                await ctx.send(f":ping_pong: Ping: `{round(s['ping'], 1)}ms`\n:arrow_down: Download: `{round(s['download']/10**6, 1)} Mbits/s`\n:arrow_up: Upload: `{round(s['upload']/10**6, 1)} Mbits/s`\n:satellite_orbital: Server: `{s['server']['sponsor']}, {s['server']['name']}, {s['server']['country']}`")

    @commands.command(name='ping', aliases=['latency', "PING", "Ping", "Pıng", "PİNG", "pıng", "LATENCY"])
    async def ping(self, ctx):
        """ Pong! """
        message = await ctx.send(":ping_pong: Pong!")
        ping = (message.created_at.timestamp() - ctx.message.created_at.timestamp()) * 1000
        await message.edit(content=f":ping_pong: Pong!\nTook: `{int(ping)}ms`\nLatency: `{int(self.bot.latency*1000)}ms`")

    @commands.command(name='botinfo' , aliases=['botstats', 'status', 'binfo'])
    async def stats(self, ctx):
        """Bot stats."""
        # Uptime
        uptime = (datetime.datetime.now() - self.bot.uptime)
        hours, rem = divmod(int(uptime.total_seconds()), 3600)
        minutes, seconds = divmod(rem, 60)
        days, hours = divmod(hours, 24)
        if days:
            time = '%s days, %s hours, %s minutes, and %s seconds' % (days, hours, minutes, seconds)
        else:
            time = '%s hours, %s minutes, and %s seconds' % (hours, minutes, seconds)

        # Embed
        em = discord.Embed(color=0x4FFCFA)
        em.set_author(name=f'{self.bot.user} Stats:', icon_url=self.bot.user.avatar_url, url='https://discord.com/api/oauth2/authorize?client_id=767832835213754409&permissions=8&scope=bot')
        em.add_field(name=':clock3: Uptime', value=f'**`{time}`**', inline=False)
        em.add_field(name=':outbox_tray: Msgs sent', value=f'**`{self.bot.messages_out:,}`**')
        em.add_field(name=':inbox_tray: Msgs received', value=f'**`{self.bot.messages_in:,}`**')
        em.add_field(name=':crossed_swords: Servers', value=f'**`{len(self.bot.guilds)}`**')
        em.add_field(name=':satellite_orbital: Server Region', value=f'**`{self.bot.region}`**')

        mem = virtual_memory()
        mem_usage = f"{mem.percent} % {mem.used / 1024 ** 2:.2f} MiB"
        em.add_field(name=u':floppy_disk: Memory usage', value=f'`{mem_usage}`')
        cpu_usage = f"{cpu_percent(1)} % {cpu_freq().current / 1000:.2f} Ghz"
        em.add_field(name=':desktop: CPU usage', value=f'`{cpu_usage}`')
        em.set_thumbnail(url="https://i.ibb.co/JK1z40M/a51b83cb114408930389ecd8f5412a9d.png")

        try:
            await ctx.send(embed=em)
        except Exception:
            await ctx.send("I don't have permission to send embeds here :disappointed_relieved:")


    @commands.command(name='py', aliases=['eval'])
    async def _eval(self, ctx, *, body):
        """Evaluates python code"""
        env = {
            'ctx': ctx,
            'bot': self.bot,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message,
            'source': inspect.getsource
        }

        def cleanup_code(content):
            """Automatically removes code blocks from the code."""
            # remove ```py\n```
            if content.startswith('```') and content.endswith('```'):
                return '\n'.join(content.split('\n')[1:-1])

            # remove `foo`
            return content.strip('` \n')

        env.update(globals())

        body = cleanup_code(body)
        stdout = io.StringIO()
        err = out = None

        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

        def paginate(text: str):
            '''Simple generator that paginates text.'''
            last = 0
            pages = []
            for curr in range(0, len(text)):
                if curr % 1980 == 0:
                    pages.append(text[last:curr])
                    last = curr
                    appd_index = curr
            if appd_index != len(text)-1:
                pages.append(text[last:curr])
            return list(filter(lambda a: a != '', pages))

        try:
            exec(to_compile, env)
        except Exception as e:
            err = await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')
            return await ctx.message.add_reaction('\u2049')

        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            err = await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
        else:
            value = stdout.getvalue()
            if ret is None:
                if value:
                    try:

                        out = await ctx.send(f'```py\n{value}\n```')
                    except:
                        paginated_text = paginate(value)
                        for page in paginated_text:
                            if page == paginated_text[-1]:
                                out = await ctx.send(f'```py\n{page}\n```')
                                break
                            await ctx.send(f'```py\n{page}\n```')
            else:
                try:
                    out = await ctx.send(f'```py\n{value}{ret}\n```')
                except:
                    paginated_text = paginate(f"{value}{ret}")
                    for page in paginated_text:
                        if page == paginated_text[-1]:
                            out = await ctx.send(f'```py\n{page}\n```')
                            break
                        await ctx.send(f'```py\n{page}\n```')

        if out:
            await ctx.message.add_reaction('✅')  # tick
        elif err:
            await ctx.message.add_reaction('❌')  # x
        else:
            await ctx.message.add_reaction('✅')

    @commands.command(hidden=True, name="announce", aliases=["sannounce", "server_announce"])
    @commands.check(this_should_be_me)
    async def announce(self, ctx, *, message):
        for guild in self.bot.guilds:
            try:
                embed = discord.Embed(title="Eg-Bot Announcement",colour = discord.Colour.green())
                embed.add_field(name = "**From Developer:**",value = ctx.message.author.name, inline=True)
                embed.add_field(name="**Message:**",value=message, inline=False)
                embed.set_image(url="https://i.ibb.co/JK1z40M/a51b83cb114408930389ecd8f5412a9d.png")
                await guild.system_channel.send(embed=embed)

            except:
                for channel in guild.text_channels:
                    if channel.permissions_for(guild.me).send_messages:
                        embed = discord.Embed(title="Eg-Bot Announcement",colour = discord.Colour.green())
                        embed.add_field(name = "**From Developer:**",value = ctx.message.author.name, inline=True)
                        embed.add_field(name="**Message:**",value=message, inline=False)
                        embed.set_image(url="https://i.ibb.co/JK1z40M/a51b83cb114408930389ecd8f5412a9d.png")
                        await channel.send(embed=embed)
                        break


    @commands.command(hidden=True, name="member_announce", aliases=["mannounce"])
    @commands.check(this_should_be_me)
    async def member_announce(self,ctx, *, message):
        output = ' '
        author = ctx.message.author
        for word in message:
            output += word

        for member in self.bot.get_all_members():
            try:
                embed = discord.Embed(title="Eg-Bot Announcement",colour = discord.Colour.green())
                embed.add_field(name = "**From Developer:**",value = author.name, inline=True)
                embed.add_field(name="**Message:**",value = output, inline=False)
                embed.set_thumbnail(url="https://i.ibb.co/JK1z40M/a51b83cb114408930389ecd8f5412a9d.png")
                await member.send(embed=embed)

            except (discord.HTTPException, discord.Forbidden,AttributeError):
                continue

        await ctx.send("Message sent :white_check_mark:")


    @commands.command(hidden=True, name="private_message", aliases=["message"])
    @commands.check(this_should_be_me)
    async def private_message(self, ctx, member:discord.Member, *,message):
        try:
            await member.send(message)
            await ctx.send("Message sent :white_check_mark:")

        except:
            await ctx.send("Failure :x:")

def setup(bot):
    bot.add_cog(Debug(bot))

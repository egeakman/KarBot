import json
import discord
from discord.ext import commands

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Info is ready.")

    """@commands.command(name='help', aliases=['h'])
    async def help(self, ctx, arg: str=''):
        "Display Help"
        embed = discord.Embed(title="My first Discord bot.", colour=discord.Colour(0x7f20a0))

        avatar_url = str(self.bot.user.avatar_url)
        embed.set_thumbnail(url=avatar_url)
        embed.set_author(name="Eg-Bot Help", url="https://discord.com/api/oauth2/authorize?client_id=792463727252602890&permissions=8&scope=bot", icon_url=avatar_url)
        embed.set_footer(text="Eg-Bot by ege.akmn#1881✨")

        if arg.strip().lower() == '-a':
            # Full version
            embed.description = 'My prefix is `.`'
            with open('help.json', 'r') as help_file:
                data = json.load(help_file)
            data = data['full']
            for key in data:
                value = '\n'.join(x for x in data[key])
                embed.add_field(name=key, value=f"```{value}```", inline=False)
        else:
            # Short version
            embed.description = 'My prefix is `.`\nType `.help -a` for detailed help.'
            with open('help.json', 'r') as help_file:
                data = json.load(help_file)
            data = data['short']
            for key in data:
                embed.add_field(name=key, value=data[key])
        try:
            await ctx.send(embed=embed)
        except Exception:
            await ctx.send("I don't have permission to send embeds here :disappointed_relieved:")"""

    @commands.command(name='invite', aliases=["ınvıte", "invıte", "ınvite", "INVITE", "İNVİTE", "INVİTE", "İNVITE", "Invite"])
    async def invite(self, ctx):
        """My invite link"""
        await ctx.send("To invite **Eg-Bot** to your server, visit: **https://cutt.ly/kjUKwu7**")

    @commands.command(name='prison', aliases=["Prison", "prıson", "Prıson", "PRISON", "PRİSON"])
    async def prison(self, ctx):
        """My help server"""
        await ctx.send("To join **Eg-Bot** 's help server, visit: **https://discord.io/prison-server**")

    @commands.command(name='support', aliases=['contact', 'owner'])
    async def support(self, ctx, *, msg: str = ""):
        """Contact bot owner"""
        if msg == "":
            return await ctx.send("Please enter a message to send towards Bot Owner", delete_after=5.0)

        embed = discord.Embed(colour=discord.Colour(0x5dadec), description=msg)
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f"{ctx.guild} : {ctx.guild.id}", icon_url=ctx.guild.icon_url)

        info = await self.bot.application_info()
        await info.owner.send(embed=embed)
        await ctx.send("Bot owner notified!")

    @commands.command(aliases=["WHOAREYOU", "Whoareyou", "ınfo", "INFO", "İNFO","whoareyou"])
    async def info(self, ctx):
        user = ctx.message.author
        await ctx.send(f"Hey {user.mention}! I'm Eg-Bot and going to be a moderator, musician and an entertainer. But I'm still learning :books:")


def setup(bot):
    bot.add_cog(Info(bot))

import os
import urllib
import requests
import io
import json
from textwrap import TextWrapper
import discord
from discord.ext import commands

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Utility is ready.")


    @commands.command(name='list')
    async def listusers(self, ctx):
        """Displays the list of connected users"""
        if not ctx.author.voice:
            return await ctx.send("You are not connected to a voice channel :mute:")
        members = ctx.author.voice.channel.members
        memnames = []
        for member in members:
            memnames.append(member.name)
        await ctx.send(f"Members in {ctx.author.voice.channel.name}:\n```\n" + "\n".join(memnames) +"\n```")


    @commands.command(name='serverinfo', aliases=['server', 'sinfo'])
    async def serverinfo(self, ctx):
        """Get server info"""

        server = ctx.guild

        # Count online members
        online = 0

        for i in server.members:
            if str(i.status) == 'online' or str(i.status) == 'idle' or str(i.status) == 'dnd':
                online += 1

        # Count channels
        tchannel_count = len([x for x in server.channels if type(x) == discord.channel.TextChannel])
        vchannel_count = len([x for x in server.channels if type(x) == discord.channel.VoiceChannel])

        # Count roles
        role_count = len(server.roles)

        # Create embed
        em = discord.Embed(title="Server Info", color=0x00CC99)
        em.add_field(name=':flying_saucer: Name', value=f'**`{server.name}`**')
        em.add_field(name=':crown: Owner', value=f'{str(ctx.guild.owner.mention)}', inline=False)
        em.add_field(name=':man_farmer: Members', value=f'**`{server.member_count}`**')
        em.add_field(name=':green_circle: Online', value=f'**`{online}`**')
        em.add_field(name=':earth_americas: Region', value=f'**`{str(server.region).title()}`**')
        em.add_field(name=':scroll: Text Channels', value=f'**`{tchannel_count}`**')
        em.add_field(name=':loud_sound: Voice Channels', value=f'**`{vchannel_count}`**')
        em.add_field(name=':shield: Verification Level', value=f'**`{str(server.verification_level).title()}`**')
        em.add_field(name=':1234: Number of roles', value=f'**`{role_count}`**')
        em.add_field(name=':man_police_officer: Highest role', value=f'**`{server.roles[-1]}`**')
        em.add_field(name=':alarm_clock: Created At', value=f"**`{server.created_at.__format__('%A, %d. %B %Y @ %H:%M:%S')}`**", inline=False)
        em.set_thumbnail(url=server.icon_url)
        em.set_footer(text='Server ID: %s' % server.id)

        try:
            await ctx.send(embed=em)
        except Exception:
            await ctx.send("I don't have permission to send embeds here :disappointed_relieved:")


    @commands.command(name='url', aliases=['shorten'])
    async def url_shorten(self, ctx, url):

        if not url.startswith('http'):
            url = 'http://' + url

        try:
            key = 'ffe283d8e3ab75a1523c013eaae15acb6423d'
            url = urllib.parse.quote(url)
            r = requests.get('http://cutt.ly/api/api.php?key={}&short={}'.format(key, url))
            json_data = json.loads(r.text)
            short_url = json_data["url"]["shortLink"]
            await ctx.send(f"Here is your shortened url: **{short_url}**")


        except:
            await ctx.send('Failed to shorten url :x:')

    @commands.command(name='tts', aliases=["text2speech", "t2s", "texttospeech"])
    async def _tts(self, ctx, *, text=''):
        """Send tts message"""
        if not text:
            return await ctx.send('Specify message to send')
        await ctx.send(content=text, tts=True)

    @commands.command(name = 'userinfo', aliases=['user', 'uinfo', 'ui'])
    async def userinfo(self, ctx, member:discord.Member):
        em=discord.Embed(title="User Info", colour=0x00CC99)
        em.add_field(name=':id: User ID', value=f'**`{member.id}`**')
        em.add_field(name=':bust_in_silhouette: Nick Name', value=f'**`{member.nick}`**')
        em.add_field(name=':chart_with_upwards_trend: Status', value=f'**`{member.status}`**')
        em.add_field(name=':loud_sound: In Voice', value=f'**`{member.voice.channel}`**')
        em.add_field(name=':man_mage: Activity', value=f'**`{member.activity}`**')
        em.add_field(name=':man_police_officer: Highest Role', value=f'**`{member.top_role}`**')
        em.add_field(name=':alarm_clock: Account Created', value=f"**`{member.created_at.__format__('%A, %d %B %Y @ %H:%M:%S')}`**", inline=False)
        if isinstance(member, discord.Member):
            em.add_field(name=':inbox_tray: Join Date', value=f"**`{member.joined_at.__format__('%A, %d %B %Y @ %H:%M:%S')}`**", inline=False)
        em.set_thumbnail(url=member.avatar_url)
        em.set_author(name=member, icon_url=member.avatar_url)
        try:
            await ctx.send(embed=em)
        except Exception:
            await ctx.send("I don't have permission to send embeds here :disappointed_relieved:")


def setup(bot):
    bot.add_cog(Utility(bot))

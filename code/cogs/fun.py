import discord
import random
import io
import json
import xkcd
import requests
import praw
import ksoftapi
from aiohttp import ClientSession
from discord.ext import commands

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        bot.client = ClientSession()
        bot.kclient = ksoftapi.Client('eyJ0IjogImFwcCIsICJrIjogImtobWFjc2lnIiwgInBrIjogNTAzMSwgIm8iOiAiMzU4Njg5MzA5MjE1MjkzNDQzIiwgImMiOiAxMjg4OTA4MX0.68634edda967e20ab72ef2592819be182fb55965a24c4cd175895452ebc16fdd')
        self.kclient = bot.kclient


    @commands.Cog.listener()
    async def on_ready(self):
        print("Fun is ready.")


    """@commands.command(name='meme', aliases=['memes'])
    async def meme(self, ctx):
        "Get Random Memes"
        try:
            async with ctx.typing():
                meme = await self.kclient.images.random_meme()
        except ksoftapi.NoResults:
            await ctx.send('Error getting meme :cry:')
        else:
            embed = discord.Embed(title=meme.title)
            embed.set_image(url=meme.image_url)
            await ctx.send(embed=embed)"""


    reddit = praw.Reddit(client_id="rjMxNnP_kVTAMw",
                         client_secret="6Y4dA6g6Nz3U_wtwSnj6R2QQdTwmsA",
                         username="egeakmn", password="egbot013579",
                         user_agent="Eg-Bot")



    @commands.command(name='xkcd')
    async def _xkcd(self, ctx):
        """Get XKCD Memes"""
        async with ctx.typing():
            c = xkcd.getRandomComic()
        embed = discord.Embed(title=c.getTitle())
        embed.set_image(url=c.getImageLink())
        embed.set_footer(text =c.getAltText())
        await ctx.send(embed=embed)


    @commands.command(name="face-palm", aliases=["fp"])
    async def face_palm(self, ctx):
        async with ctx.typing():
            r = requests.get('https://some-random-api.ml/animu/face-palm')
            json_data = json.loads(r.text)
            image = json_data["link"]

            em = discord.Embed()
            em.set_image(url=image)
            await ctx.send(embed=em)

    @commands.command(name="wink")
    async def wink(self, ctx):
        async with ctx.typing():
            r = requests.get('https://some-random-api.ml/animu/wink')
            json_data = json.loads(r.text)
            image = json_data["link"]

            em = discord.Embed()
            em.set_image(url=image)
            await ctx.send(embed=em)

    @commands.command(name="pat")
    async def pat(self, ctx):
        async with ctx.typing():
            r = requests.get('https://some-random-api.ml/animu/pat')
            json_data = json.loads(r.text)
            image = json_data["link"]

            em = discord.Embed()
            em.set_image(url=image)
            await ctx.send(embed=em)

    @commands.command(name="hug")
    async def hug(self, ctx):
        async with ctx.typing():
            r = requests.get('https://some-random-api.ml/animu/hug')
            json_data = json.loads(r.text)
            image = json_data["link"]

            em = discord.Embed()
            em.set_image(url=image)
            await ctx.send(embed=em)

    """@commands.command(name="meme")
    async def hug(self, ctx):
        async with ctx.typing():
            r = requests.get('https://some-random-api.ml/meme')
            json_data = json.loads(r.text)
            image = json_data["image"]
            caption = json_data["caption"]

            em = discord.Embed(title=(f"Random Meme"), color=discord.Colour.purple())
            em.set_image(url=image)
            em.set_footer(text=f"{caption}")
            await ctx.send(embed=em)"""

    @commands.command(name="meme", aliases=["memes", "sj"])
    async def meme(self, ctx, *, subred = "meme"):
        subreddit = reddit.subreddit(subred)
        top = subreddit.top(limit = 50)
        all_subs = []
        for submission in top:
            all_subs.append(submission)

        random_sub = random.choice(all_subs)

        caption = random_sub.title
        image = random_sub.url

        em = discord.Embed(title=caption, color=discord.Colour.random())
        em.set_image(url=image)

    @commands.command(name="fact", aliases=["animal"])
    async def fact(self, ctx, animal : str):
        async with ctx.typing():
            if (animal:= animal.lower()) in ("dog", "cat", "panda", "fox", "birb", "koala", "racoon", "kangaroo"):

                r_a = requests.get('https://some-random-api.ml/animal/{}'.format(animal))
                json_data = json.loads(r_a.text)
                fact = json_data["fact"]
                image = json_data["image"]

                c_animal = animal.capitalize()

                em = discord.Embed(title=(f"**{c_animal} Fact**"), color=discord.Colour.blue())
                em.add_field(name='Fact: ', value=fact, inline=False)
                em.set_image(url=image)
                em.set_footer(text="Random facts about animals.")
                em.set_thumbnail(url="https://i.ibb.co/JK1z40M/a51b83cb114408930389ecd8f5412a9d.png")
                await ctx.send(embed=em)

            else:
                await ctx.send(f'No facts are available for {animal}. If you are looking for bird facts try it with "birb".')


    @commands.command()
    async def hi(self, ctx):
        user = ctx.message.author
        await ctx.send(f"Hey {user.mention}! What's up?")


    @commands.command(aliases=["gn"])
    async def goodnight(self, ctx):
        user = ctx.message.author
        await ctx.send(f"Good night {user.mention} :zzz:")


    @commands.command(aliases=["gm"])
    async def goodmorning(self, ctx):
        user = ctx.message.author
        await ctx.send(f"Good morning {user.mention} :sunrise:")


    @commands.command()
    async def whoami(self, ctx):
        user = ctx.message.author
        await ctx.send(f"You are you {user.mention}!")


    @commands.command()
    async def wow(self, ctx):
        await ctx.send("https://tenor.com/view/what-wut-shocked-chris-farley-gif-4172416")


    @commands.command(aliases=["h5"])
    async def high5(self, ctx):
        await ctx.send("https://tenor.com/view/high-five-spongebob-patrick-jumping-high-five-gif-7888580")


def setup(bot):
    bot.add_cog(Fun(bot))

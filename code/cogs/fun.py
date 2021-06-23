import discord
import random
import io
from PIL import Image
from io import BytesIO
import json
from discord.ext.commands.core import has_permissions
import xkcd
import requests
from aiohttp import request
from discord.ext import commands

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        print("Fun is ready.")


    @commands.command()
    async def whoisthebest(self,ctx):
        """Shows who is the best."""
        await ctx.send(f"Of course {ctx.author.mention}!!")
    @commands.command()
    async def napim(self,ctx):


        random_sj=["ooo hawli", "reis bu ağırdı :flushed:", "sjsjsjsj", "kardeşim soktun lafı", "komki", "e-eritin...",
        "https://tenor.com/view/napim-otuzbir-mizaj-gif-19220089",
        "https://tenor.com/view/napim-gif-21127885",
        "https://tenor.com/view/napim-mizah-mizaj-cool-gif-19273345",
        "https://tenor.com/view/napimbugrabasgan-napim-bugrabasgan-bugra-gif-19548224",
        "https://tenor.com/view/napim-napim1-napim2-napim3-gif-20093240",
        "https://tenor.com/view/napim-gif-20052788"]
        await ctx.send(random.choice(random_sj))
    @commands.command()
    async def punch(self,ctx,member:discord.Member):
        """Punch someone you mention."""
        if ctx.author.id == member.id:
            emb = discord.Embed(description="**" + ctx.author.mention +" punched {0.mention}, ".format(member) + "Why did you punch yourself?**",color=0xff0000)
            emb.set_image(url="https://media.tenor.com/images/5dd7bacf7f4839d2487606b947441021/tenor.gif")
        elif member.id==833701547879170109:
            emb=discord.Embed(description=f"**Taste my punch and cry {ctx.author.mention}!!**")
            emb.set_image(url="https://media.tenor.com/images/5dd7bacf7f4839d2487606b947441021/tenor.gif")
        else:
            emb = discord.Embed(description="**" + ctx.author.mention +" punched {0.mention}, ".format(member) + "{0.mention} Be Careful!!**".format(member),color=0xff0000)
            emb.set_image(url="https://media.tenor.com/images/5dd7bacf7f4839d2487606b947441021/tenor.gif")
        await ctx.send(embed=emb)


    @commands.command()
    async def kill(self,ctx,member:discord.Member):
        """Kill someone you mention."""
        if ctx.author.id ==member.id:
            emb = discord.Embed(description="**Everything will be okay. I promise :pleading_face:**",color=0xff0000)

        else:
            emb = discord.Embed(description="**" + ctx.author.mention +" killed {0.mention}**".format(member),color=0xff0000)
            emb.set_image(url="https://media.tenor.com/images/3d68ffaf557461c2e1a30d3e587a73e5/tenor.gif")
        await ctx.send(embed=emb)


    @commands.command(aliases=["roll-dice", "roll"])
    async def dice(self,ctx):
        """Rolls a dice."""
        dicenum = random.randint(1,6)
        if dicenum == 1:
            roll ="https://i.ibb.co/zsJ7wM2/zar1.jpg"
        elif dicenum == 2:
            roll ="https://i.ibb.co/Z2CvLXb/zar2.jpg"
        elif dicenum == 3:
            roll ="https://i.ibb.co/9h4KPcq/zar3.jpg"
        elif dicenum == 4:
            roll ="https://i.ibb.co/z5yvqk2/zar4.jpg"
        elif dicenum == 5:
            roll = "https://i.ibb.co/PQLNFZS/zar5.jpg"
        elif dicenum == 6:
            roll = "https://i.ibb.co/bgWcKqV/zar6.jpg"
        await ctx.send(roll)


    @commands.command()
    async def choice(self,ctx,*,message):
        """Chooses one from values ​​separated by spaces."""
        message = message.split(" ")
        await ctx.send(f"My choice: ||{random.choice(message)}||")


    @commands.command(name='xkcd_memes',aliases=["meme", "memes", "xkcd"])
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

    @commands.command()
    async def wink(self,ctx,member:discord.Member):
        """Wink someone you mention."""
        url="https://some-random-api.ml/animu/wink"
        async with request("GET",url,headers={}) as response:
            if response.status==200:
                data = await response.json()
                embed = discord.Embed(description=f"**{member.mention}, {ctx.author.mention} winked you.**",color=0xff0000)

                embed.set_image(url=data["link"])
                await ctx.send(embed=embed)


    @commands.command()
    async def pikachu(self,ctx):
        """Sends random pikachu videos."""
        url="https://some-random-api.ml/img/pikachu"
        async with request("GET",url,headers={}) as response:
            data = await response.json()
            await ctx.send(data["link"])


    @commands.command()
    async def hug(self,ctx,member:discord.Member):
        """Hug someone you mention."""
        url="https://some-random-api.ml/animu/hug"
        if ctx.author.id==member.id:
            async with request("GET",url,headers={}) as response:
                data = await response.json()
                embed = discord.Embed(description=f"**{ctx.author.mention}, KarBot hugged you.**",color=0xff0000)
                embed.set_image(url=data["link"])
                await ctx.send(f"**{ctx.author.mention}, I'm by your side.**")

        else:
            async with request("GET",url,headers={}) as response:
                data = await response.json()
                embed=discord.Embed(description=f"**{member.mention}, {ctx.author.mention}  hugged you.**",color=0xff0000)
                embed.set_image(url=data["link"])
        await ctx.send(embed=embed)

    @commands.command()
    async def spank(self,ctx,member:discord.Member):
        """Spank someone you mention."""

        if ctx.author.id == member.id:
            embed=discord.Embed(description=f"**Spanking yourself is good.**")
            embed.set_image(url="https://media1.tenor.com/images/3c161bd7d6c6fba17bb3e5c5ecc8493e/tenor.gif?itemid=5196956")
        elif member.id==833701547879170109:
            embed=discord.Embed(description=f"**You can't spank me, I'm spanking you {ctx.author.mention}!!**")
            embed.set_image(url="https://media1.tenor.com/images/3c161bd7d6c6fba17bb3e5c5ecc8493e/tenor.gif?itemid=5196956")
        else:
            embed=discord.Embed(description=f"**{ctx.author.mention} spanks {member.mention}**")
            embed.set_image(url="https://media1.tenor.com/images/3c161bd7d6c6fba17bb3e5c5ecc8493e/tenor.gif?itemid=5196956")
        await ctx.send(embed=embed)

    @commands.command()
    async def pat(self,ctx,member:discord.Member):
        """Pat someone you mention."""
        if ctx.author.id==member.id:
            url = "https://some-random-api.ml/animu/pat"
            async with request("GET",url,headers={}) as response:
                data = await response.json()
                embed=discord.Embed(description=f"**Don't worry. KarBot patted {member.mention}**")
                embed.set_image(url=data["link"])

        else:
            url = "https://some-random-api.ml/animu/pat"
            async with request("GET",url,headers={}) as response:
                data = await response.json()
                embed=discord.Embed(description=f"**{ctx.author.mention} patted {member.mention}**")
                embed.set_image(url=data["link"])
        await ctx.send(embed=embed)

    @commands.command()
    async def wanted(self,ctx,member:discord.Member=None):
        """Run, They are coming."""
        if member == None:
            member = ctx.author
        wanted = Image.open("wanted.jpg")
        asset = member.avatar_url_as(size=128)
        data = BytesIO(await asset.read())
        pfp = Image.open(data)
        pfp = pfp.resize((401,401))
        wanted.paste(pfp,(245,445))
        wanted.save("wanted.jpg")
        await ctx.send(file = discord.File("wanted.jpg"))

    @commands.command()
    async def shit(self,ctx,member:discord.Member=None):
        """Surprise ;)"""
        if member==None:
            member=ctx.author
        bok = Image.open("shit.jpg")
        asset=member.avatar_url_as(size=128)
        data=BytesIO(await asset.read())
        pfp = Image.open(data)
        pfp=pfp.resize((384,368))
        bok.paste(pfp,(260,380))
        bok.save("shit.jpg")
        await ctx.send(file=discord.File("shit.jpg"))


    @choice.error
    async def choice_error(self,ctx,error):
        if isinstance(error,commands.MissingRequiredArgument):
            await ctx.send("Send me options!")
        elif isinstance (error,commands.CommandInvokeError):
            await ctx.send("Make sure you are using the command correctly.")
        elif isinstance(error,commands.BadArgument):
            await ctx.send("Make sure you are using the command correctly.")


    @wanted.error
    async def wanted_error(self,ctx,error):

        if isinstance (error,commands.CommandInvokeError):
            await ctx.send("Make sure you are using the command correctly.")
        elif isinstance(error,commands.BadArgument):
            await ctx.send("Make sure you are using the command correctly.")

    @kill.error
    async def kill_error(self,ctx,error):
        if isinstance(error,commands.MissingRequiredArgument):
            await ctx.send("Please mention someone you wanna kill.")
        elif isinstance (error,commands.CommandInvokeError):
            await ctx.send("Make sure you are using the command correctly.")
        elif isinstance(error,commands.BadArgument):
            await ctx.send("Make sure you are using the command correctly.")

    @shit.error
    async def shit_error(self,ctx,error):

        if isinstance (error,commands.CommandInvokeError):
            await ctx.send("Make sure you are using the command correctly.")
        elif isinstance(error,commands.BadArgument):
            await ctx.send("Make sure you are using the command correctly.")

    @wink.error
    async def wink_error(self,ctx,error):
        if isinstance(error,commands.MissingRequiredArgument):
            await ctx.send("Please mention someone you wanna wink.")
        elif isinstance (error,commands.CommandInvokeError):
            await ctx.send("Make sure you are using the command correctly.")
        elif isinstance(error,commands.BadArgument):
            await ctx.send("Make sure you are using the command correctly.")

    @hug.error
    async def hug_error(self,ctx,error):
        if isinstance(error,commands.MissingRequiredArgument):
            await ctx.send("Please mention someone you wanna hug.")
        elif isinstance (error,commands.CommandInvokeError):
            await ctx.send("Make sure you are using the command correctly.")
        elif isinstance(error,commands.BadArgument):
            await ctx.send("Make sure you are using the command correctly.")

    @spank.error
    async def spank_error(self,ctx,error):
        if isinstance(error,commands.MissingRequiredArgument):
            await ctx.send("Please mention someone you wanna spank.")
        elif isinstance (error,commands.CommandInvokeError):
            await ctx.send("Make sure you are using the command correctly.")
        elif isinstance(error,commands.BadArgument):
            await ctx.send("Make sure you are using the command correctly.")

    @pat.error
    async def pat_error(self,ctx,error):
        if isinstance(error,commands.MissingRequiredArgument):
            await ctx.send("Please mention someone you wanna pat.")
        elif isinstance (error,commands.CommandInvokeError):
            await ctx.send("Make sure you are using the command correctly.")
        elif isinstance(error,commands.BadArgument):
            await ctx.send("Make sure you are using the command correctly.")

    @punch.error
    async def hit_error(self,ctx,error):
        if isinstance(error,commands.MissingRequiredArgument):
            await ctx.send("Please mention someone you wanna punch.")
        elif isinstance (error,commands.CommandInvokeError):
            await ctx.send("Make sure you are using the command correctly.")
        elif isinstance(error,commands.BadArgument):
            await ctx.send("Make sure you are using the command correctly.")


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
        await ctx.send("ROOT :robot:")

    @commands.command(hidden=True)
    async def uname(self, ctx):
        await ctx.send("Thought you could hack me?")

    @commands.command(hidden=True)
    async def cd(self, ctx):
        await ctx.send("Why are ya messing with ma directories bro??")


    @commands.command(hidden=True,name="31",aliases=["osbi", "otuz bir", "ozbi", "otuzbir"])
    async def _31(self, ctx):

        random_sj=["sj", "sjsj", "sjsjsjsj", "NE DİYO BU CHAT???", "sen demek osbi", "mizah tufanı",
        "kahkaha şöleni", "d-dostum sen çok komiksin", "sj dostum", "bruh", "step bro im stuck",
        "sensin o kardeşim", "şey mi dostum", "https://tenor.com/view/31mizah-ka%C4%9F%C4%B1thane-%C3%B6zg%C3%BCr-deniz-gif-19382605",
        "https://tenor.com/view/31-%C3%A7ko-komiq-31%C3%A7ko-komik-31%C3%A7ok-komik-31cok-komik-gif-19310158",
        "https://tenor.com/view/31sj%C3%A7ok-komik-eh%C3%BC-gif-20556435",
        "https://tenor.com/view/31-gif-18668786"]

        await ctx.send(random.choice(random_sj))


    @commands.command()
    async def wow(self, ctx):
        await ctx.send("https://tenor.com/view/what-wut-shocked-chris-farley-gif-4172416")

    @commands.command(aliases=["h5","hi5"])
    async def high5(self, ctx):
        await ctx.send("https://tenor.com/view/high-five-spongebob-patrick-jumping-high-five-gif-7888580")


def setup(bot):
    bot.add_cog(Fun(bot))

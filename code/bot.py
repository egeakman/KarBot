import discord
import random
import os
import io
import ksoftapi
import json
from utils import canvas
from aiohttp import ClientSession
import datetime
from discord.ext import commands, tasks
from itertools import cycle

def get_prefix(bot, message):
    with open("prefixes.json", "r") as p:
        prefixes = json.load(p)

    return prefixes[str(message.guild.id)]

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix = get_prefix, guild_subscriptions=True, intents=intents)
status = cycle([".help", ".invite", ".prison", "My Instagram: @ege.akmn"])
bot.uptime = datetime.datetime.now()
bot.messages_in = bot.messages_out = 0
bot.region = 'Paris, FR'
#bot.remove_command('help')

@bot.event
async def on_ready():
    status_changer.start()
    bot.kclient = ksoftapi.Client('eyJ0IjogImFwcCIsICJrIjogImtobWFjc2lnIiwgInBrIjogNTAzMSwgIm8iOiAiMzU4Njg5MzA5MjE1MjkzNDQzIiwgImMiOiAxMjg4OTA4MX0.68634edda967e20ab72ef2592819be182fb55965a24c4cd175895452ebc16fdd')
    bot.client = ClientSession()
    print("Bot is ready.")

@bot.event
async def on_guild_join(guild):
    with open("prefixes.json", "r") as p:
        prefixes = json.load(p)

    prefixes[str(guild.id)] = "!"

    with open("prefixes.json", "w") as p:
        json.dump(prefixes, p, indent=4)

    try:
        await guild.system_channel.send('Hey there! Thank you for adding me!\nMy default prefix is `.`\nYou can always change it by `.prefix` command.\nStart by typing `.help`')

    except:
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                await channel.send('Hey there! Thank you for adding me!\nMy default prefix is `.`\nYou can always change it by `.prefix` command.\nStart by typing `.help`')
                break

@bot.event
async def on_guild_remove(guild):
    with open("prefixes.json", "r") as p:
        prefixes = json.load(p)

    prefixes.pop(str(guild.id))

    with open("prefixes.json", "w") as p:
        json.dump(prefixes, p, indent=4)

@bot.event
async def on_member_join(member):
        try:
            await member.guild.system_channel.send(f'Hey there {member.mention}, welcome to {str(member.guild.name)}! {member.guild.owner.mention} hopes you enjoy this server :cowboy:')

        except:
            pass

@bot.event
async def on_member_remove(member):
    try:
        await member.guild.system_channel.send(f"Why did you leave :pensive:  {member.mention} I'll miss you...")

    except:
        pass
        #for channel in member.guild.text_channels:
            #if channel.permissions_for(member.guild.me).send_messages:
                #await channel.send(f"Why did you leave :pensive:  {member.mention} I'll miss you...")
                #break


@bot.event
async def on_message(message):
    # Sent message
    if message.author.id == bot.user.id:
        if hasattr(bot, 'messages_out'):
            bot.messages_out += 1
    # Received message (Count only commands messages)
    elif message.content.startswith('.'):
        if hasattr(bot, 'messages_in'):
            bot.messages_in += 1

    await bot.process_commands(message)


@tasks.loop(seconds=8)
async def status_changer():
    activity = discord.Game(next(status))
    await bot.change_presence(status=discord.Status.online, activity=activity)


@bot.event
async def on_command_error(ctx, error):
    pass


def this_should_be_me(ctx):
    return ctx.author.id == 358689309215293443


@bot.command(hidden=True)
@commands.check(this_should_be_me)
async def load(ctx, extension):
    bot.load_extension(f"cogs.{extension}")
    await ctx.send("Done!")


@bot.command(hidden=True)
@commands.check(this_should_be_me)
async def unload(ctx, extension):
    bot.unload_extension(f"cogs.{extension}")
    await ctx.send("Done!")


for filename in os.listdir("./code/cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")

bot.run("NzkyNDYzNzI3MjUyNjAyODkw.X-eFWw.t5chVRrkAZXH7Dr9v7aRhZhHBok")

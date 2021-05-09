import discord
import os
import io
import json
import datetime
from discord.ext import commands, tasks
from itertools import cycle

def get_prefix(bot, message):
    with open("prefixes.json", "r") as p:
        prefixes = json.load(p)

    return prefixes[str(message.guild.id)]

intents = discord.Intents(messages=True,guilds = True,reactions = True,members = True,presences = True)
bot = commands.Bot(command_prefix = get_prefix, guild_subscriptions=True, intents=intents)
status = cycle([".help"])
bot.uptime = datetime.datetime.now()
bot.messages_in = bot.messages_out = 0
bot.region = 'Istanbul, TR'
#bot.remove_command('help')

@bot.event
async def on_ready():
    status_changer.start()
    print("Bot is ready.")

@bot.event
async def on_guild_join(guild):
    with open("prefixes.json", "r") as p:
        prefixes = json.load(p)

    prefixes[str(guild.id)] = "."

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
        await member.guild.system_channel.send(f"Why did you leave :pensive:  {member.display_name} I'll miss you...")

    except:
        pass


@bot.event
async def on_message(message):
    # Sent message
    if message.author.id == bot.user.id:
        if hasattr(bot, 'messages_out'):
            bot.messages_out += 1
    # Received message (Count only commands messages)
    elif message.content.startswith(get_prefix(bot, message)):
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
    return ctx.author.id == 579592895380586496 or ctx.author.id == 358689309215293443


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

bot.run("ODMzNzAxNTQ3ODc5MTcwMTA5.YH2LEg.SNXnObiCyJSNT_WiIZ6lGXvVCFo")

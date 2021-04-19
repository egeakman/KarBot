from discord.ext import commands
import json
import os
import io
from discord.ext import commands, tasks

class Settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Settings is ready.")


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def prefix(self, ctx, prefix):
        with open("prefixes.json", "r") as p:
            prefixes = json.load(p)

        prefix_lowercase = prefix.lower()
        is_letter = prefix_lowercase.islower()

        def hasNumbers(inputString):
             return any(char.isdigit() for char in inputString)

        is_digit = hasNumbers(prefix)

        if is_letter == True or is_digit == True:
            prefix = prefix + " "

        prefixes[str(ctx.guild.id)] = prefix

        with open("prefixes.json", "w") as p:
            json.dump(prefixes, p, indent=4)

        await ctx.send(f"Prefix changed to: `{prefix}`")

    @prefix.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Sorry you are not allowed to use this command. Only admins can use this :x:")
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Usage of `prefix` command: {your_current_prefix} prefix {new_prefix}\nExample: `.prefix !`")

def setup(bot):
    bot.add_cog(Settings(bot))

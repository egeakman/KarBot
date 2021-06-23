import discord
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.Cog.listener()
    async def on_ready(self):
        print("Moderation is ready.")

    #Clear
    @commands.command(aliases=["CLEAR", "Clear"])
    async def clear(self, ctx, amount : int):
            await ctx.channel.purge(limit=amount + 1)
            await ctx.send(f"Deleted {amount} messages", delete_after=5)

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Sorry you are not allowed to use this command.")
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please type an amount of messages to delete.")

    #Kick
    @commands.command(aliases=["kıck", "KICK", "KİCK", "Kick"])
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member : discord.Member, *, reason="something"):
        await member.kick(reason=reason)
        await ctx.send(f"{member} kicked as a result of {reason}")

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Sorry you are not allowed to use this command.")
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please type a user to kick.")

    #Ban
    @commands.command(aliases=["BAN", "Ban"])
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member : discord.Member, *, reason="something"):
        await member.ban(reason=reason)
        await ctx.send(f"{member} banned as a result of {reason}")

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Sorry you are not allowed to use this command.")
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please type a user to ban.")

    #Unban
    @commands.command(aliases=["UNBAN", "Unban"])
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split("#")
        for ban_entry in banned_users:
            user = ban_entry.user
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f"{user.name}#{user.discriminator} unbanned. Behave boi!")
                return

    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Sorry you are not allowed to use this command.")
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please type a user to unban.")


    @commands.command()
    async def clone(self,ctx):
        """Clone the text channel."""
        if ctx.author.guild_permissions.manage_channels:
            await ctx.channel.clone()
            await ctx.send(f"**{ctx.channel} is cloned.**")
        else:
            await ctx.send("You don't have perms to use that command.")


def setup(client):
    client.add_cog(Moderation(client))

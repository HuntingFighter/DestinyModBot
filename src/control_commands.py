from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
import db
import re

class ControlCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @has_permissions(administrator = True)
    async def setControlChannel(self, ctx):
        """Set Servers Control channel for the bot (can be identical to posting and wish channel)"""
        server_id = ctx.message.guild.id
        channel_id = ctx.message.channel.id
        if not db.isServerRegistered(server_id):
            print("Adding Server {0}".format(server_id))
            db.addServer(server_id, channel_id)
        else:
            print("Updating commands channel for server {0}".format(server_id))
            db.setControlChannel(server_id, channel_id)
        await ctx.send("```Bot command channel was set to {0}```".format(ctx.message.channel.name))

    @setControlChannel.error
    async def setControlChannel_error(self, ctx, error):
        print("Control channel setting denied.")
        print(error)
        if isinstance(error, MissingPermissions):
            await ctx.send(":x: Only administrators can use this command.")

    @commands.command()
    @has_permissions(administrator = True)
    async def setControlRole(self, ctx, role):
        """Sets Servers Control role for the bot, only people with this role can change the bots settings. If a role has already been set it will replace the old role."""
        if db.isServerRegistered(ctx.message.guild.id):
            print(role)
            roleId = ""
            if re.search("<@&[0-9]*>", role):
                roleId = re.sub("<@&", "", role)
                roleId = re.sub(">", "", roleId)
                db.setControlRole(ctx.message.guild.id, roleId)
                await ctx.send("```Bot Control role has been set```")
            if roleId == "":
                await ctx.send("```Please ping the role you want to set as control role.```")
        else:
            await ctx.send("```Please add a Control channel first using !setControlChannel```")

    @setControlRole.error
    async def setControlRole_error(self, ctx, error):
        print("Control role setting denied.")
        if isinstance(error, MissingPermissions):
            await ctx.send(":x: Only administrators can use this command.")

    @commands.command()
    @has_permissions(administrator = True)
    async def unsetCommandRole(self, ctx):
        """Removes server control role for the bot"""
        if db.isServerRegistered(ctx.message.guild.id):
            db.unsetRoleId(ctx.message.guild.id)
            await ctx.send("```Removed Control Role, to set a new Control Role use !setControlRole and ping the role```")
        else:
            await ctx.send("```Please add a Control channel first using !setControlChannel```")

    @unsetCommandRole.error
    async def removeCommandRole_error(self, ctx, error):
        print("Command role removal denied.")
        if isinstance(error, MissingPermissions):
            await ctx.send(":x: Only administrators can use this command.")

    @commands.command()
    async def setModDisplayChannel(self, ctx):
        """Command executed in channel that should be the mod display channel, can only be used by people with a bot control role. For better visibility, nobody should be able to write in this channel."""
        if db.isServerRegistered(ctx.message.guild.id):
            db.setInfoChannel(ctx.message.guild.id, ctx.message.channel.id)
            await ctx.send("```Set the display channel for the server```")
        else:
            await ctx.send("```Please add a Control channel first using !setControlChannel```")

    @commands.command()
    async def setWishesChannel(self, ctx):
        """Command executed in channel that should be the wish / info channel, can only be used by people with a bot control role."""
        if db.isServerRegistered(ctx.message.guild.id):
            db.setWishesChannel(ctx.message.guild.id, ctx.message.channel.id)
            await ctx.send("```Set the wish channel for the server```")
        else:
            await ctx.send("```Please add a Control channel first using !setControlChannel```")

    @commands.command()
    @has_permissions(administrator = True)
    async def removeServer(self, ctx, confirmation = None):
        """Removes the bot from the server. "WARNING, removing the server will delete the wishlists everyone who is not registered on another server as well that as this bot."""
        if confirmation == "CONFIRM":
            db.removeServer(ctx.message.guild.id)
            await ctx.send("All data for your server has been deleted from the bots databases.")
        else:
            await ctx.send("```WARNING, removing the server will delete all data saved for this server. Wishlists of people on the server are not removed, they can remove their wishlists by sending !clearWishlist to the bot. If the bot gets kicked from the server all data is automatically removed at next reset. To confirm deletion please type '!removeServer CONFIRM'```")

    @removeServer.error
    async def removeServer_error(self, ctx, error):
        print("Command server removal denied.")
        if isinstance(error, MissingPermissions):
            await ctx.send(":x: Only administrators can use this command.")

def setup(bot):
    bot.add_cog(ControlCommands(bot))

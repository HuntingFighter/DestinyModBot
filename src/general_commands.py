from discord.ext import commands
from discord.abc import PrivateChannel
import db
import mod_management

class GeneralCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def addWish(self, ctx, *mod_name_parts):
        """Add wish to your wishlist"""
        author_id = ctx.message.author.id
        validChannel = False
        if ctx.message.guild is not None:
            server_id = ctx.message.guild.id
            wish_channel_id = db.getWishesChannel(server_id)
            validChannel = ctx.message.channel.id == wish_channel_id
        if validChannel or isinstance(ctx.message.channel, PrivateChannel):
            mod_name = " ".join(mod_name_parts[:])
            if db.isModExistant(mod_name):
                if not db.hasWishOnWishlist(author_id, mod_name):
                    db.addToWishlist(author_id, mod_name)
                    await ctx.send("```Added {0} to your wishlist.```".format(mod_name))
                else:
                    await ctx.send("```That mod is already on your wishlist.```")
            else:
                await ctx.send("```The mod you are looking for does not exist.```")

    @commands.command()
    async def removeWish(self, ctx, *mod_name_parts):
        """Remove wish from your wishlist"""
        validChannel = False
        if ctx.message.guild is not None:
            server_id = ctx.message.guild.id
            wish_channel_id = db.getWishesChannel(server_id)
            validChannel = ctx.message.channel.id == wish_channel_id
        if validChannel or isinstance(ctx.message.channel, PrivateChannel):
            author_id = ctx.message.author.id
            mod_name = " ".join(mod_name_parts[:])
            if db.isModExistant(mod_name):
                if db.hasWishOnWishlist(author_id, mod_name):
                    db.removeFromWishlist(author_id, mod_name)
                    await ctx.send("```Removed {0} from your wishlist.```".format(mod_name))
                else:
                    await ctx.send("```That mod is not on your wishlist.```")
            else:
                await ctx.send("```The mod you are looking for does not exist.```")

    @commands.command()
    async def clearWishlist(self, ctx):
        """Clears your whole wishlist and removes you from Bots database"""
        validChannel = False
        if ctx.message.guild is not None:
            server_id = ctx.message.guild.id
            wish_channel_id = db.getWishesChannel(server_id)
            validChannel = ctx.message.channel.id == wish_channel_id
        if validChannel or isinstance(ctx.message.channel, PrivateChannel):
            author_id = ctx.message.author.id
            await db.clearWishlist(author_id)
            await ctx.send("```Your wishlist has been cleared.```")

    @commands.command()
    async def wishes(self, ctx):
        """Shows all your current wishes"""
        validChannel = False
        if ctx.message.guild is not None:
            server_id = ctx.message.guild.id
            wish_channel_id = db.getWishesChannel(server_id)
            validChannel = ctx.message.channel.id == wish_channel_id
        if validChannel or isinstance(ctx.message.channel, PrivateChannel):
            author_id = ctx.message.author.id
            wishes = db.getWishes(author_id)
            wishlist = "```Your current wishlist is:\n"
            print(wishes)
            for wish in wishes:
                wishlist += "- {0}\n".format(wish[0])

            wishlist += "To remove items from your wishlist, use !removeWish, to clear your wishlist use !clearWishlist.```"

            await ctx.send(wishlist)

    @commands.command()
    async def mods(self, ctx):
        """Shows Mods that are currently sold"""
        validChannel = False
        if ctx.message.guild is not None:
            server_id = ctx.message.guild.id
            wish_channel_id = db.getWishesChannel(server_id)
            validChannel = ctx.message.channel.id == wish_channel_id
        if validChannel or isinstance(ctx.message.channel, PrivateChannel):
            await ctx.send(mod_management.getModText())

    @commands.command()
    async def forceUpdate(self, ctx):
        """Test Command"""
        await mod_management.updateMods(ctx.bot)

def setup(bot):
    bot.add_cog(GeneralCommands(bot))

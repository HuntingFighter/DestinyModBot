from discord.ext import commands
import discord.errors
import mod_management
import db
import os

bot = commands.Bot(command_prefix='!', description='Banshee-44 and Ada-1 Mods')
startup_extensions = ["control_commands", "general_commands"]


@bot.command(hidden=True)
async def test(ctx):
    await ctx.send('<:arc:839121229708656640> Banshee is selling some mods, this test message was sent by ' + ctx.message.author.display_name)


@bot.command(hidden=True)
async def broadcastPatchnotes(ctx):
    if ctx.message.author.id == 205400021686943744:
        channels = db.getAllInfoChannels()
        print(channels)
        for channel in channels:
            try:
                channelInt = int(channel[0])
                dcChannel = bot.get_channel(channelInt)
                if dcChannel is None:
                    dcChannel = await bot.fetch_channel(channelInt)
                if dcChannel is not None:
                    await dcChannel.send('```Destiny Mod Bot Patch Notes:\n- Changed infrastructure to Database (This should greatly improve performance)\n- Added Info Channel and Control Channel. Your currently Registered Channel will automatically be assigned the Mod Display, Wish and Control Channel, a Server Admin can set the Wish channel individually through !setWishesChannel. This can be the same but be advised to use a different channel so the mods are always cleanly visible\n'
                                     '- Control Channel in future will be used to configure settings of the bot (Should he show Ada, Banshee, Xur, etc.)\n- Changed wishlist saving so wishlists are not bound to a server anymore (you can now see your wishlists on any server with this bot)\n- As long as you are on a Server with this bot you can now edit your Wishlists through Private Chat to the bot\n'
                                     '- Mods in the mod message now have their Element and Category listed as well\n- Bot is prepared for Ada-1 integration as soon as the endpoints for this go live\n- Mods are now queried quicker after daily Reset, you should receive your notifications much faster now\n\nThank you for using Destiny Mod Bot and may you get your Mods as fast as possible :)\n\n'
                                     'PS: I did a full recode of the whole bot in the progess of those changes so please bear with me if there is hickups, I\'ll do my best to prevent them and remove them asap. Migration of Wishlist Data is pretty much 100%, if you made any changes within the last 2-3 hours please check if they are still on the list.```')
            except discord.errors.NotFound:
                print("Channel was deleted, checking Server Access")
                try:
                    guild = bot.get_guild(channel[1])
                    if guild is None:
                        guild = await bot.fetch_guild(channel[1])
                except discord.errors.Forbidden:
                    print("Bot was removed from a server, deleting data")
                    db.removeServer(channel[1])


@bot.command(hidden=True)
async def broadcastMods(ctx):
    if ctx.message.author.id == 205400021686943744:
        await mod_management.broadcastMods(bot)


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await mod_management.updateMods(bot)

if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))
    bot.run(os.environ["D_TOKEN"])

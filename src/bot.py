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

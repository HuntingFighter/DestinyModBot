import db
import requests
import json
import asyncio
from discord.errors import Forbidden, NotFound
from datetime import datetime, timedelta

lastUpdated = ''


def getModText():
    activeMods = db.getActiveModsBanshee()

    modMessage = "``Banshee is currently selling:``\n"

    energy = activeMods[0][1]
    if energy == "Any" or energy is None:
        modMessage += "<:neutral:839121253717114970>"
    if energy == "Solar":
        modMessage += "<:solar:839121175480500224>"
    if energy == "Arc":
        modMessage += "<:arc:839121229708656640>"
    if energy == "Void":
        modMessage += "<:void:839121204857274389>"

    modMessage += " **`{0}` ({1})**\n".format(activeMods[0][0], activeMods[0][2])

    energy = activeMods[1][1]
    if energy == "Any" or energy is None:
        modMessage += "<:neutral:839121253717114970>"
    if energy == "Solar":
        modMessage += "<:solar:839121175480500224>"
    if energy == "Arc":
        modMessage += "<:arc:839121229708656640>"
    if energy == "Void":
        modMessage += "<:void:839121204857274389>"

    modMessage += " **`{0}` ({1})**\n\n".format(activeMods[1][0], activeMods[1][2])

    activeMods = db.getActiveModsAda()

    if len(activeMods) == 2:
        energy = activeMods[0][1]
        modMessage += "``Ada is currently selling:``\n"
        if energy == "Any" or energy is None:
            modMessage += "<:neutral:839121253717114970>"
        if energy == "Solar":
            modMessage += "<:solar:839121175480500224>"
        if energy == "Arc":
            modMessage += "<:arc:839121229708656640>"
        if energy == "Void":
            modMessage += "<:void:839121204857274389>"

        modMessage += " **`{0}` ({1})**\n".format(activeMods[0][0], activeMods[0][2])

        energy = activeMods[1][1]
        if energy == "Any" or energy is None:
            modMessage += "<:neutral:839121253717114970>"
        if energy == "Solar":
            modMessage += "<:solar:839121175480500224>"
        if energy == "Arc":
            modMessage += "<:arc:839121229708656640>"
        if energy == "Void":
            modMessage += "<:void:839121204857274389>"

        modMessage += " **`{0}` ({1})**\n".format(activeMods[1][0], activeMods[1][2])

    modMessage += "``The mods update every day at 17:00 UTC.``"
    return modMessage


async def getCurrentMods():
    response = json.loads(requests.get("https://api.destinyinsights.com/mods").text)
    global lastUpdated
    mods = db.getActiveModsBanshee()
    modnames = []
    if len(mods) == 2:
        modnames = [mods[0][0], mods[1][0]]
    if response['metadata']['lastUpdated'] != lastUpdated and response['inventory'][0]['name'] not in modnames and response['inventory'][1]['name'] not in modnames:
        lastUpdated = response['metadata']['lastUpdated']
        mod1 = response['inventory'][0]['itemHash']
        mod2 = response['inventory'][1]['itemHash']
        db.setActiveModsBanshee(mod1, mod2)
        return True
    return False


async def broadcastMods(bot):
    channels = db.getAllInfoChannels()
    print(channels)
    for channel in channels:
        try:
            channelInt = int(channel[0])
            dcChannel = bot.get_channel(channelInt)
            if dcChannel is None:
                dcChannel = await bot.fetch_channel(channelInt)
            if dcChannel is not None:
                await dcChannel.send(getModText())
        except NotFound:
            print("Channel was deleted, checking Server Access")
            try:
                guild = bot.get_guild(channel[1])
                if guild is None:
                    guild = await bot.fetch_guild(channel[1])
            except Forbidden:
                print("Bot was removed from a server, deleting data")
                db.removeServer(channel[1])
        except Forbidden:
            print("Bot channel permissions have been revoked, deleting data")
            db.removeServer(channel[1])

    currentModsBanshee = db.getActiveModsBanshee()
    currentModsAda = db.getActiveModsAda()

    allWishers = []

    if len(currentModsBanshee) == 2:
        for mod in currentModsBanshee:
            wishers = db.getWishers(mod[0])
            print(mod[0])
            print(wishers)
            for wisher in wishers:
                if wisher not in allWishers:
                    allWishers.append(wisher)

    if len(currentModsAda) == 2:
        for mod in currentModsAda:
            wishers = db.getWishers(mod[0])
            for wisher in wishers:
                if wisher not in allWishers:
                    allWishers.extend([wisher])

    for wisher in allWishers:
        print(allWishers)
        print(wisher)
        dWisher = bot.get_user(int(wisher[0]))
        if dWisher is None:
            dWisher = await bot.fetch_user(int(wisher[0]))
        if dWisher is not None:
            modMessage = "``Your personal Wishlist Notification is here:``\n\n"

            wishersB0 = db.getWishers(currentModsBanshee[0][0])
            wishersB1 = db.getWishers(currentModsBanshee[1][0])
            wishersA0 = []
            wishersA1 = []

            if len(currentModsAda) == 2:
                wishersA0 = db.getWishers(currentModsAda[0][0])
                wishersA1 = db.getWishers(currentModsAda[1][0])

            if wisher in wishersB0 or wisher in wishersB1:
                modMessage = "``Banshee-44 is currently selling:``\n"
                if wisher in wishersB0:
                    mod = currentModsBanshee[0]
                    energy = mod[1]
                    if energy == "Any" or energy is None:
                        modMessage += "<:neutral:839121253717114970>"
                    if energy == "Solar":
                        modMessage += "<:solar:839121175480500224>"
                    if energy == "Arc":
                        modMessage += "<:arc:839121229708656640>"
                    if energy == "Void":
                        modMessage += "<:void:839121204857274389>"
                    modMessage += " **`{0}` ({1})**\n".format(mod[0], mod[2])

                if wisher in wishersB1:
                    mod = currentModsBanshee[1]
                    energy = mod[1]
                    if energy == "Any" or energy is None:
                        modMessage += "<:neutral:839121253717114970>"
                    if energy == "Solar":
                        modMessage += "<:solar:839121175480500224>"
                    if energy == "Arc":
                        modMessage += "<:arc:839121229708656640>"
                    if energy == "Void":
                        modMessage += "<:void:839121204857274389>"
                    modMessage += " **`{0}` ({1})**\n".format(mod[0], mod[2])


            if wisher in wishersA0 or wisher in wishersA1:
                modMessage = "``Ada-1 is currently selling:``\n"
                if wisher in wishersA0:
                    mod = currentModsBanshee[0]
                    energy = mod[1]
                    if energy == "Any" or energy is None:
                        modMessage += "<:neutral:839121253717114970>"
                    if energy == "Solar":
                        modMessage += "<:solar:839121175480500224>"
                    if energy == "Arc":
                        modMessage += "<:arc:839121229708656640>"
                    if energy == "Void":
                        modMessage += "<:void:839121204857274389>"
                    modMessage += " **`{0}` ({1})**\n".format(mod[0], mod[2])

                if wisher in wishersA1:
                    mod = currentModsBanshee[1]
                    energy = mod[1]
                    if energy == "Any" or energy is None:
                        modMessage += "<:neutral:839121253717114970>"
                    if energy == "Solar":
                        modMessage += "<:solar:839121175480500224>"
                    if energy == "Arc":
                        modMessage += "<:arc:839121229708656640>"
                    if energy == "Void":
                        modMessage += "<:void:839121204857274389>"
                    modMessage += " **`{0}` ({1})**\n".format(mod[0], mod[2])


            modMessage += "``The mods will be available for 10 Mod Components each until tomorrow 17:00 UTC.``\n"
            modMessage += "``You can remove the mods by using !removeWish <mod name> in here or in any Wish channel of a server running this bot.``\n"
            modMessage += "``You can clear your wishlist and remove all data saved about you by the bot by using !clearWishlist in here or in any Wish channel of a server running this bot.``\n"

            try:
                await dWisher.send(modMessage)
            except Forbidden:
                print("User is no longer on a server with Mod Bot, data is being deleted.")
                db.clearWishlist(wisher[0])
        else:
            print("User no longer exists")
            db.clearWishlist(wisher[0])




async def updateMods(bot):
    print("Update Mods called")
    result = await getCurrentMods()
    if result:
        now = datetime.utcnow()
        date = now.strftime("%Y%m%d")
        date += "170100"
        nextReset = datetime.strptime(date, "%Y%m%d%H%M%S")
        if nextReset < now:
            nextReset = nextReset + timedelta(days=1)
        tomorrowResetTime = (nextReset - now).total_seconds()
        await broadcastMods(bot)
        print("Next refresh in {0} Seconds".format(tomorrowResetTime))
        await asyncio.sleep(tomorrowResetTime)
        await updateMods(bot)
    else:
        print("Next refresh in 60 Seconds")
        await asyncio.sleep(60)
        await updateMods(bot)


import db
import requests
import json
import asyncio
import topggAPI
from discord.errors import Forbidden, NotFound
from datetime import datetime, timedelta

lastUpdated = ''

def getSingleModText(mod):
    modMessage = ""
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
    return modMessage


def getModText():
    activeMods = db.getActiveModsBanshee()

    modMessage = "``Banshee is currently selling:``\n"

    for mod in activeMods:
        modMessage += getSingleModText(mod)

    activeMods = db.getActiveModsAda()

    if len(activeMods) > 0:
        modMessage += "``Ada is currently selling:``\n"

        for mod in activeMods:
            modMessage += getSingleModText(mod)

    modMessage += "``The mods update every day at 17:00 UTC.``"
    return modMessage


async def getCurrentMods():
    response = json.loads(requests.get("https://api.destinyinsights.com/mods").text)
    mods = db.getActiveModsBanshee()
    modnames = []
    for mod in mods:
        modnames.append(mod[0])
    newMods = response['inventory']

    isChange = False
    for mod in newMods:
        if mod['name'] not in modnames:
            isChange = True

    if isChange:
        db.setActiveModsBanshee(newMods)
        return True
    return False


async def broadcastMods(bot):
    channels = db.getAllInfoChannels()
    print(channels)
    for channel in channels:
        try:
            if channel[0] is not None:
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

    if len(currentModsBanshee) != 0:
        for mod in currentModsBanshee:
            wishers = db.getWishers(mod[0])
            print(mod[0])
            print(wishers)
            for wisher in wishers:
                if wisher not in allWishers:
                    allWishers.append(wisher)

    if len(currentModsAda) != 0:
        for mod in currentModsAda:
            wishers = db.getWishers(mod[0])
            for wisher in wishers:
                if wisher not in allWishers:
                    allWishers.append(wisher)

    wishersBanshee = []
    wishersAda = []

    for mod in currentModsBanshee:
        wishersBanshee.append(db.getWishers(mod[0]))

    for mod in currentModsAda:
        wishersAda.append(db.getWishers(mod[0]))


    for wisher in allWishers:
        dWisher = bot.get_user(int(wisher[0]))
        if dWisher is None:
            dWisher = await bot.fetch_user(int(wisher[0]))
        if dWisher is not None:
            hasBansheeModsOnWishlist = False
            hasAdaModsOnWishlist = False

            for modwishers in wishersBanshee:
                if wisher in modwishers:
                    hasBansheeModsOnWishlist = True

            for modwishers in wishersAda:
                if wisher in modwishers:
                    hasAdaModsOnWishlist = True

            modMessage = "``Your personal Wishlist Notification is here:``\n\n"

            modCounter = 0
            if hasBansheeModsOnWishlist:
                modMessage += "``Banshee-44 is currently selling:``\n"
                for modwishers in wishersBanshee:
                    if wisher in modwishers:
                        modMessage += getSingleModText(currentModsBanshee[modCounter])
                    modCounter += 1
                modMessage += "\n"

            modCounter = 0
            if hasAdaModsOnWishlist:
                modMessage += "``Ada-1 is currently selling:``\n"
                for modwishers in wishersAda:
                    if wisher in modwishers:
                        modMessage += getSingleModText(currentModsAda[modCounter])
                    modCounter += 1

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
    while True:
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
            print("Next refresh in {0} Seconds, sending data to top.gg API".format(tomorrowResetTime))
            await topggAPI.sendTopGGApiInfo(bot)
            await asyncio.sleep(tomorrowResetTime)
            await updateMods(bot)
        else:
            print("Next refresh in 60 Seconds")
            await topggAPI.sendTopGGApiInfo(bot)
            await asyncio.sleep(60)


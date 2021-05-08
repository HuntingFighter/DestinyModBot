# DestinyModBot

A Bot that lists the Armor and Weapond Mods Banshee-44 sells right now as well as allows to sign up for notifications. If you sign up for notifications you will get a PM whenever Banshee-44 sells the Mod you are looking for so you never miss out on a Mod again.

Use !register to register a channel for usage with this bot, then everyone can use !add and !remove to add or remove wishes. All things you wish for have to be valid names of Mods in Destiny 2 that you will then be notified whenever Banshee-44 sells them.
Available Commands:

    !help show help message
    !setControlChannel sets the Control channel for Destiny Mod Bot and registers the server
    !setModDisplayChannel sets the channel where Mods should be shown
    !setWishesChannel sets the channel where people can state their wishes. All these three can be the same, however, I highly advise to put the Display Channel to a dedicated channel.
    !removeServer removes the server and all associated data from the Bot
    !addWish mod-name add mod to your notification list
    !removeWish mod-name remove mod from your notification list
    !wishes show a list of your current wishes
    !mods shows Mods currently available

Shortly after daily Reset (17:00 UTC) the bot will check for the new mods available at Banshee-44 and inform all people via DM that registered for one or both of the mods sold at the respective day. It will also send a message to the registered Channel containing the currently available modules without a ping.

Disclaimer: Eventhough I will do my best to keep this up and running all the time, downtimes may happen and I not responsible if you miss out an offer because you solely relied on this bot.

Big bot update has been done just now. If you see any irregularities please let me know so I can fix them asap.

TL;DR last TWAB: Bungie will change Armor mods to Ada-1 next season. I will do my best to have the Bot reflect this as soon as it goes live, also data migration is in the works rn so I hope for massive performance improvements soon.


# Fiddling yourself
To test with the bot yourself create a .env file on the base level of the project setting the following variables:

    D_TOKEN=Your Discord Bot Token

    DB_HOST=Your Database Host
    DB_DB=Your Database name
    DB_USER=Your Database user
    DB_PASSWORD=Your database Password
    DB_AUTOCOMMIT=True
    DB_PORT=Your Database Port
    DB_PW_ROOT=Your Database Root Password

You will also need to set the root password in the init_db.sh as well as user credentials and db name in init_db.sql.

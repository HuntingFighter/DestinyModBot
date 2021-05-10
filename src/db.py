import mysql.connector
import os

db = mysql.connector.connect(
    host = os.environ["DB_HOST"],
    database = os.environ["DB_DB"],
    user = os.environ["DB_USER"],
    password = os.environ["DB_PASSWORD"],
    autocommit = os.environ["DB_AUTOCOMMIT"],
    port = os.environ["DB_PORT"]

)

cursor = db.cursor(buffered=True)


def addServer(server_id, control_channel_id):
    cursor.execute("INSERT INTO servers (server_id, control_channel_id) VALUES (%(server_id)s, %(control_channel_id)s)", {'server_id': server_id, 'control_channel_id': control_channel_id})


def setControlChannel(server_id, control_channel_id):
    cursor.execute("UPDATE servers SET control_channel_id = %(control_channel_id)s WHERE server_id = %(server_id)s", { 'control_channel_id': control_channel_id, 'server_id': server_id })


def setInfoChannel(server_id, info_channel_id):
    cursor.execute("UPDATE servers SET info_channel_id = %(info_channel_id)s WHERE server_id = %(server_id)s", { 'info_channel_id': info_channel_id, 'server_id': server_id })


def setControlRole(server_id, control_role_id):
    cursor.execute("UPDATE servers SET control_role_id = %(control_role_id)s WHERE server_id = %(server_id)s", { 'control_role_id': control_role_id, 'server_id': server_id })


def setWishesChannel(server_id, wishes_channel_id):
    cursor.execute("UPDATE servers SET wishes_channel_id = %(wishes_channel_id)s WHERE server_id = %(server_id)s", { 'wishes_channel_id': wishes_channel_id, 'server_id': server_id })


def unsetRoleId(server_id):
    cursor.execut("UPDATE servers SET control_role = null WHERE server_id = %(server_id)s", { 'server_id': server_id })


def removeServer(server_id):
    cursor.execute("DELETE FROM servers WHERE server_id = %(server_id)s", { 'server_id': server_id })


def isServerRegistered(server_id):
    cursor.execute("SELECT server_id FROM servers WHERE server_id = %(server_id)s", { 'server_id': server_id })
    result = cursor.fetchone()
    return result is not None


def isModExistant(mod_name):
    cursor.execute("SELECT id FROM mods WHERE LOWER(name) = LOWER(%(mod_name)s)", { 'mod_name': mod_name })
    result = cursor.fetchone()
    return result is not None


def hasWishOnWishlist(user_id, mod_name):
    cursor.execute("SELECT id FROM wishes WHERE user_id = %(user_id)s AND mod_id IN (SELECT id FROM mods WHERE LOWER(name) = LOWER(%(mod_name)s))", { 'user_id': user_id, 'mod_name': mod_name })
    result = cursor.fetchone()
    return result is not None


def addToWishlist(user_id, mod_name):
    cursor.execute("SELECT id FROM mods WHERE LOWER(name) = LOWER(%(mod_name)s)", { 'mod_name': mod_name })
    mod_id = cursor.fetchone()[0]
    cursor.execute("INSERT INTO wishes (user_id, mod_id) VALUES (%(user_id)s, %(mod_id)s)", { 'user_id': user_id, 'mod_id': mod_id })


def removeFromWishlist(user_id, mod_name):
    cursor.execute("DELETE FROM wishes WHERE user_id = %(user_id)s AND mod_id IN (SELECT id FROM mods WHERE LOWER(name) = LOWER(%(mod_name)s))", { 'user_id': user_id, 'mod_name': mod_name})


def clearWishlist(user_id):
    cursor.execute("DELETE FROM wishes WHERE user_id = %(user_id)s", { 'user_id': user_id })


def getWishes(user_id):
    cursor.execute("SELECT name FROM mods WHERE id IN (SELECT mod_id FROM wishes WHERE user_id = %(user_id)s)", { 'user_id': user_id })
    return cursor.fetchall()


def getActiveModsBanshee():
    cursor.execute("SELECT name, energy_type, mod_type FROM mods WHERE id in (SELECT mod_id FROM current_mods WHERE vendor = 'Banshee')")
    return cursor.fetchall()


def getActiveModsAda():
    cursor.execute("SELECT name, energy_type, mod_type FROM mods WHERE id in (SELECT mod_id FROM current_mods WHERE vendor = 'Ada')")
    return cursor.fetchall()


def getActiveModIdsBanshee():
    cursor.execute("SELECT mod_id FROM current_mods WHERE vendor = 'Banshee'")
    return cursor.fetchall()


def getActiveModIdsAda():
    cursor.execute("SELECT mod_id FROM current_mods WHERE vendor = 'Ada'")
    return cursor.fetchall()


def setActiveModsBanshee(newMods):
    cursor.execute("DELETE FROM current_mods WHERE vendor = 'Banshee'")
    for mod in newMods:
        cursor.execute("INSERT INTO current_mods (mod_id, vendor) VALUES (%(mod_id)s, 'Banshee')", { 'mod_id': mod["itemHash"] })


def setActiveModsAda(newMods):
    cursor.execute("DELETE FROM current_mods WHERE vendor = 'Ada'")
    for mod in newMods:
        cursor.execute("INSERT INTO current_mods (mod_id, vendor) VALUES (%(mod_id)s, 'Ada')", { 'mod_id': mod["itemHash"] })


def getWishesChannel(server_id):
    cursor.execute("SELECT wishes_channel_id FROM servers WHERE server_id = %(server_id)s", { 'server_id': server_id })
    result = cursor.fetchone()
    if result is not None:
        result = int(result[0])
    else:
        result = 0
    return result

def getControlChannel(server_id):
    cursor.execute("SELECT control_channel_id FROM servers WHERE server_id = %(server_id)s", { 'server_id': server_id })
    result = cursor.fetchone()
    if result is not None:
        result = int(result[0])
    else:
        result = 0
    return result

def getInfoChannel(server_id):
    cursor.execute("SELECT info_channel_id FROM servers WHERE server_id = %(server_id)s", { 'server_id': server_id })
    result = cursor.fetchone()
    if result is not None:
        result = int(result[0])
    else:
        result = 0
    return result

def getControlRole(server_id):
    cursor.execute("SELECT control_role_id FROM servers WHERE server_id = %(server_id)s", { 'server_id': server_id })
    result = cursor.fetchone()
    if result is not None:
        result = int(result[0])
    else:
        result = 0
    return result

def getAllInfoChannels():
    cursor.execute("SELECT info_channel_id, server_id FROM servers")
    result = cursor.fetchall()
    return result

def getWishers(mod_name):
    cursor.execute("SELECT user_id FROM wishes WHERE mod_id IN (SELECT id FROM mods WHERE name = %(mod_name)s)", { 'mod_name': mod_name })
    return cursor.fetchall()
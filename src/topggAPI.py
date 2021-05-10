import os
import requests

async def sendTopGGApiInfo(bot):
    print(requests.post("https://top.gg/api//bots/{0}/stats".format(os.environ["TOP_GG_BOT_ID"]), headers={'Authorization': os.environ["TOP_GG_BOT_TOKEN"]}, data={'server_count': len(bot.guilds), 'shard_count': bot.shard_count}).text)

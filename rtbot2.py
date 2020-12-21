import discord, os, asyncio, aiomysql
from discord.ext import commands

loop = asyncio.get_event_loop()

async def connect_db():
    pool = await aiomysql.create_pool(
        host='arpa.kro.kr',
        user='rtbot',
        password='infinite2018!!rtbot',
        db='rtbot',
        charset='utf8',
        autocommit=True
    )
    return pool
    
pool = loop.run_until_complete(connect_db())

intents = discord.Intents.all()
client = commands.AutoShardedBot(command_prefix=['알티야 ','ㅇ!','알','알 '],intents=intents)
client.pool = pool

for ext in filter(lambda x: x.endswith('.py') and not x.startswith('_'), os.listdir('./exts')):
    client.load_extension('exts.' + os.path.splitext(ext)[0])

client.run('NjYxNDc3NDYwMzkwNzA3MjAx.Xgr-5A.mQ479UgeAc92mDKtHzrREgdUoUg')

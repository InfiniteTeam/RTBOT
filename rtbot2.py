import discord,os
from discord.ext import commands

client = commands.AutoShardedBot(command_prefix=['알티야 ','ㅇ!','알','알 '])

for ext in filter(lambda x: x.endswith('.py') and not x.startswith('_'), os.listdir('./exts')):
    client.load_extension('exts.' + os.path.splitext(ext)[0])

client.run('Njg3ODMxMTIwNDIyNzY0NTU0.Xmrepg.9yHnIMbk7kD_hnkcEohWc0nc-s4')

import discord,os,json,traceback,datetime,asyncio
from discord.ext import commands, tasks
from rtbot_utils import errors
from random import randint

client = commands.AutoShardedBot(command_prefix=['알티야 ','ㅇ!','알','알 '])
start_time = datetime.datetime.utcnow()
with open("./data/remember.json", "r", encoding='UTF8') as db_json:  relist = json.load(db_json)

def get_embed(title, description='', color=0xCCFFFF): 
    return discord.Embed(title=title,description=description,color=color)

def format_perm_by_name(name):
    names = { 'administrator': '관리자', 'add_reactions': '반응 추가하기' }
    try: rst = names[name]
    except KeyError: rst = name
    return rst

def find_missing_perms_by_tbstr(tbstr: str):
    perms = []
    if 'add_reaction' in tbstr: perms.append('add_reactions')
    return perms

@client.event
async def bg_change_playing():
    for v in [f"알티봇 V3.4.3", "'알티야 도움'로 봇명령어 알아보기", f"{len(client.guilds)} Servers│{len(client.users)} Users"]: 
        await asyncio.gather(client.change_presence(activity=discord.Game(v)),asyncio.sleep(15))
    client.loop.create_task(bg_change_playing())

@client.event
async def on_guild_join(guild):
    await client.get_channel(735563383277092874).send(f"<a:ok:689877466705297444>추가됨\n{guild.name} **{len(guild.members)}**\n현재 서버수 : {len(client.guilds)}")

@client.event
async def on_guild_remove(guild):
    await client.get_channel(735563383277092874).send(f"<a:no:689877428142604390>제거됨\n{guild.name}\n현재 서버수 : {len(client.guilds)}")

@client.event
async def on_ready():
    print("==================\nRTBOT ONLINE\n==================")
    client.loop.create_task(bg_change_playing())

@client.event
async def on_command_error(ctx: commands.Context, error: Exception):
    allerrs = (type(error), type(error.__cause__))
    tb = traceback.format_exception(type(error), error, error.__traceback__)
    err = [line.rstrip() for line in tb]
    errstr = '\n'.join(err)
    if commands.errors.MissingRequiredArgument in allerrs:
        return
    elif isinstance(error, discord.NotFound):
        return
    elif isinstance(error, commands.errors.BadArgument):
        await ctx.send(embed=get_embed("<a:no:698461934613168199> | 명령어 양식을 지켜주세요!","",0xFF0000))
        return
    elif isinstance(error, errors.NotMaster):
        await ctx.send(embed=get_embed("<a:no:698461934613168199> | 봇에 엑세스할 권한이 부족합니다!","필요한 권한 : `봇 어드민`",0xFF0000))
        return
    elif isinstance(error, errors.NotRegistered):
        await ctx.send(embed=get_embed('<a:no:698461934613168199> | 가입 되어 있지 않습니다!',"<알티야 가입> 으로 가입해주세요", 0xFF0000))
        return
    elif isinstance(error, errors.NoMoney):
        await ctx.send(embed=get_embed('<a:no:698461934613168199> | 돈이 부족합니다!','',0xff0000))
        return
    elif isinstance(error, errors.AlreadyRegistered):
        await ctx.send(embed=get_embed('<a:no:698461934613168199> | 이미 가입 되어 있습니다!',"", 0xFF0000))
        return
    elif isinstance(error, errors.morethan1):
        await ctx.send(embed=get_embed('<a:no:698461934613168199> | 1원 이상의 정수값을 입력해주세요!',"", 0xFF0000))
        return
    elif errors.ParamsNotExist in allerrs:
        await ctx.send(embed=get_embed(f'<a:no:698461934613168199> | 존재하지 않는 명령 옵션입니다: {", ".join(str(error.__cause__.param))}',f'`알티야 도움` 명령으로 전체 명령어를 확인할 수 있어요.',0xFF0000))
        return
    elif isinstance(error, commands.errors.CommandNotFound):
        return
    elif isinstance(error, commands.errors.CommandOnCooldown):
        if int(error.retry_after) > 1:
            await ctx.send(embed=get_embed("<a:no:698461934613168199> | 명령어를 조금만 천천히 써주세요!",'{:.2f}초만 기다려주세요!'.format(error.retry_after),0xFF0000))
        return
    elif isinstance(error, (commands.errors.CheckFailure, commands.errors.MissingPermissions)):
        perms = [format_perm_by_name(perm) for perm in error.missing_perms]
        await ctx.send(embed=get_embed('<a:no:698461934613168199> | 멤버 권한 부족!',f'{ctx.author.mention}, 이 명령어를 사용하려면 다음과 같은 길드 권한이 필요합니다!\n`'+ '`, `'.join(perms) + '`',0xFF0000))
        return
    elif errors.ParamsNotExist in allerrs:
            embed = discord.Embed(title=f'❓ 존재하지 않는 명령 옵션입니다: {", ".join(str(error.__cause__.param))}', description=f'`알티야 도움` 명령으로 전체 명령어를 확인할 수 있어요.', color=self.color['error'])
            await ctx.send(embed=embed)
            return
    elif isinstance(error.__cause__, discord.HTTPException):
        if error.__cause__.code == 50013:
            if ctx.channel.permissions_for(ctx.guild.me).send_messages:
                missings = find_missing_perms_by_tbstr(errstr)
                fmtperms = [format_perm_by_name(perm) for perm in missings]
                await ctx.send(embed=get_embed('<a:no:698461934613168199> | 봇 권한 부족!',f'이 명령어를 사용하는 데 필요한 봇의 권한이 부족합니다!\n**부족한 권한** : `{",".join(fmtperms)}`',0xFF0000))
                return
            else:
                await ctx.author.send(embed=get_embed('<a:no:698461934613168199> | 봇 권한 부족!', f"봇에게 **{ctx.channel.name}** 채널에 메세지를 보낼 권한이 없습니다.", 0xFF0000))
                return
        elif error.__cause__.code == 50035:
            await ctx.send(embed=get_embed('<a:no:698461934613168199> | 메시지 전송 실패','보내려고 하는 메시지가 너무 길어 전송에 실패했습니다.',0xff0000))
            return
        elif error.__cause__.code == 50007:
            embed = discord.Embed(title='❗ 메시지 전송 실패', description='DM(개인 메시지)으로 메시지를 전송하려 했으나 실패했습니다.\n혹시 DM이 비활성화 되어 있지 않은지 확인해주세요!', color=self.color['error'])
            await ctx.send(ctx.author.mention, embed=embed)
            return
        else:
            await ctx.send('오류 코드: ' + str(error.__cause__.code))
            return
    if ctx.author.id == 467666650183761920:
        await ctx.send(embed=get_embed('<a:no:698461934613168199> | **ERROR**!',f'무언가 오류가 발생했습니다!\n```python\n{error}```\n오류가 기록되었습니다. 나중에 개발자가 확인하고 처리하게 됩니다.',0xFF0000))
    else:
        await ctx.send(embed=get_embed('<a:no:698461934613168199> | **ERROR**!','알수없는 오류발생. 관리자에게 문의해보세요!',0xff0000))
        await client.get_channel(728788620000886854).send(embed=get_embed('<a:no:698461934613168199> | **ERROR**!',f'무언가 오류가 발생했습니다!\n```python\n{error}```\n오류가 기록되었습니다. 나중에 개발자가 확인하고 처리하게 됩니다.',0xFF0000))

@client.command(name='로드')
async def extload(ctx, extension):
    if ctx.author.id != 467666650183761920: raise errors.NotMaster
    try: client.load_extension(f'exts.{extension}')
    except: await ctx.send(f"LOAD\n<a:no:702745889751433277> {extension}")
    else: await ctx.send(f"LOAD\n<a:ok:702745889839775816> {extension}")

@client.command(name='언로드')
async def extunload(ctx, extension):
    if ctx.author.id != 467666650183761920: raise errors.NotMaster
    try: client.unload_extension(f'exts.{extension}')
    except: await ctx.send(f"UNLOAD\n<a:no:702745889751433277> {extension}")
    else: await ctx.send(f"UNLOAD\n<a:ok:702745889839775816> {extension}")

@client.command(name='리')
async def extreload(ctx):
    if ctx.author.id != 467666650183761920: raise errors.NotMaster
    try:
        for filename in os.listdir("./exts"):
            if filename.endswith('.py'):
                client.reload_extension(f'exts.{filename[:-3]}')
        await ctx.send(f"<a:ok:702745889839775816> RELOAD")
    except: await ctx.send("ERROR")

@client.command(name='리로드')
async def extreload(ctx, extention):
    if ctx.author.id != 467666650183761920: raise errors.NotMaster
    if (not extention) or ('*' in extention):
        for filename in os.listdir("./exts"):
            if filename.endswith('.py'):
                client.reload_extension(f'exts.{filename[:-3]}')
        await ctx.send(f"<a:ok:702745889839775816> RELOAD")
    else:
        try:  client.reload_extension(f'exts.{extention}')
        except: await ctx.send(f"RELOAD\n<a:no:702745889751433277> {extention}")
        else: await ctx.send(f"RELOAD\n<a:ok:702745889839775816> {extention}")

for filename in os.listdir("./exts"):
    if filename.endswith('.py'):
        client.load_extension(f'exts.{filename[:-3]}')

client.run('NjYxNDc3NDYwMzkwNzA3MjAx.XxhHsw.BnlrH7lKcJNP_igIlF1tugCxG64')
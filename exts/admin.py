import discord,os,json,random,datetime,requests,bs4,asyncio,typing,io
from discord.ext import commands 
from utils import errors

with open("./data/noticechannel.json", "r", encoding='UTF8') as db_json: noticedb = json.load(db_json)

def get_embed(title, description='', color=0xCCFFFF):
    embed=discord.Embed(title=title,description=description,color=color)
    return embed

class admincmds(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command(name='공지채널')
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def _notice(self, ctx):
        if str(ctx.guild.id) in noticedb.keys():
            if noticedb[str(ctx.guild.id)] == ctx.channel.id:
                await ctx.send(embed=discord.Embed(title=f'❓ 이미 이 채널이 공지채널로 설정되어 있습니다!', color=0xff0000))
                return
            embed = get_embed('📢 | 공지채널 설정', f'**현재 공지채널은 <#{noticedb[str(ctx.guild.id)]}> 로 설정되어 있습니다.**\n<#{ctx.channel.id}> 을 공지채널로 설정할까요?\n20초 안에 선택해주세요.')
        else:    
            embed = get_embed('📢 | 공지채널 설정', f'<#{ctx.channel.id}> 을 공지채널로 설정할까요?\n20초 안에 선택해주세요.')
        msg = await ctx.send(embed=embed)
        for rct in ['⭕', '❌']:
            await msg.add_reaction(rct)
        def notich_check(reaction, user):
            return user == ctx.author and msg.id == reaction.message.id and str(reaction.emoji) in ['⭕', '❌']
        try:
            reaction, user = await self.client.wait_for('reaction_add', timeout=20, check=notich_check)
        except asyncio.TimeoutError:
            await ctx.send(embed=discord.Embed(title='⏰ | 시간이 초과되었습니다!', color=0xff0000))
            return
        else:
            em = str(reaction.emoji)
            if em == '⭕':
                noticedb[str(ctx.guild.id)]=ctx.channel.id
                with open("./data/noticechannel.json", "w", encoding='utf-8') as database_json: database_json.write(json.dumps(noticedb, ensure_ascii=False, indent=4))
                await ctx.send(embed=get_embed(f'📢 | 공지 채널을 성공적으로 설정했습니다!',f'이제 <#{ctx.channel.id}> 채널에 공지를 보냅니다.'))
            elif em == '❌':
                await ctx.send(embed=discord.Embed(title=f'❌ 취소되었습니다.', color=0xff0000))

    @commands.command(name='eval')
    async def _eval(self, ctx, *, arg):
        if ctx.author.id != 467666650183761920: raise errors.NotMaster
        with open("./data/userdatabase.json", "r", encoding='UTF8') as db_json: userdb = json.load(db_json)
        try: await ctx.send(embed=get_embed('관리자 기능 - Eval',f"📤 OUTPUT```{eval(arg)}```"))
        except Exception as a: await ctx.send(embed=get_embed('관리자 기능 - Eval',f"📤 EXCEPT```{a}```",0xFF0000))

    @commands.command(name='await')
    async def _awa_it(self, ctx, *, arg):
        if ctx.author.id != 467666650183761920: raise errors.NotMaster
        try: await eval(arg)
        except Exception as a: await ctx.send(embed=get_embed('관리자 기능 - Await Eval',f"📤 EXCEPT```{a}```",0xFF0000))

    @commands.command(name='공지보내')
    async def _notice_send(self, ctx, *, arg):
        if ctx.author.id != 467666650183761920: raise errors.NotMaster
        lis =["SUCCEED LIST"]
        faillis = ["FAIL LIST"]
        sendctrlpannel = await ctx.send(embed=get_embed("공지 전송중",""))
        for s in self.client.guilds:
            sendedserver = s.name
            schannel = ''
            if str(s.id) in noticedb.keys():
                schannel=self.client.get_channel(noticedb[str(s.id)])
            else:
                for channel in s.text_channels:
                    if channel.permissions_for(s.me).send_messages:
                        freechannel = channel
                        if '공지' in channel.name and '봇' in channel.name:
                            schannel = channel
                            break
                        elif 'noti' in channel.name.lower() and 'bot' in channel.name.lower():
                            schannel = channel
                            break
                        elif '공지' in channel.name:
                            schannel = channel
                            break
                        elif 'noti' in channel.name.lower():
                            schannel = channel
                            break
                        elif '봇' in channel.name:
                            schannel = channel
                            break
                        elif 'bot' in channel.name.lower():
                            schannel = channel
                            break
                if schannel == '':
                    schannel = freechannel
            try: 
                await schannel.send(embed=get_embed("<a:waiting:712170404869046334> ｜ 알티봇 3.6 Algedi (알게디) 대규모 업데이트 공지",arg+"\n\n모든 문의,건의는 [알티봇 서포트](https://discord.gg/hTZxtbC) 에서 해주세요.\n[알티봇 초대하기](https://discordapp.com/api/oauth2/authorize?client_id=661477460390707201&permissions=8&scope=bot) "))
                lis.append('성공 '+sendedserver)
            except: 
                faillis.append('실패 '+sendedserver)
            await sendctrlpannel.edit(embed=get_embed("공지 전송중",f"성공 : {len(lis)-1}\n실패 : {len(faillis)-1}"))
        await ctx.send("성공")
        logfile = discord.File(fp=io.StringIO("\n".join(lis)+"\n\n"+"\n".join(faillis)), filename='notilog.log')
        await ctx.send(file=logfile)
        

def setup(client):
    client.add_cog(admincmds(client))

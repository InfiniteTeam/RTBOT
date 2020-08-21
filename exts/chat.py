import discord,os,json,random,datetime,requests,bs4,asyncio,typing
from discord.ext import commands 

start_time = datetime.datetime.utcnow()

with open("./data/emblem.json","r", encoding='UTF-8') as db_json: emblem = json.load(db_json)

def get_embed(title, description='', color=0xCCFFFF):
    embed=discord.Embed(title=title,description=description,color=color)
    return embed

class chat(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="주사위")
    async def chat_dice(self, ctx):
        await ctx.send(embed=get_embed("주사위 : "+[":one:",":two:",":three:",":four:",":five:",":six:"][random.randint(0,5)]))

    @commands.command(name='정보')
    async def chat_info(self, ctx):
        embed = discord.Embed(title="🏷️ | **RT BOT**",description=f"RT BOT Made By **TH_PHEC#0001**\n> Made With Discord.py\n> Ver. Beta 3.4\n> Helpers. **미래#2374**\n**{len(self.client.guilds)}** SERVERS | **{len(self.client.users)}** USERS", color=0xCCffff)
        embed.set_footer(text="TEAM Infinite®️",icon_url='https://cdn.discordapp.com/icons/689375730483855389/89eb7bfc0dabc59dcda58e733818a4c5.webp?size=1024')
        embed.set_thumbnail(url=self.client.user.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(name='핑')
    async def chat_ping(self, ctx):
        ping = round(1000 * self.client.latency,2)
        if ping <= 100: pinglevel = '🔵 매우좋음'
        elif 100 < ping <= 250: pinglevel = '🟢 양호함'
        elif 250 < ping <= 400: pinglevel = '🟡 보통'
        elif 400 < ping <= 550: pinglevel = '🔴 나쁨'
        else: pinglevel = '⚫ 매우나쁨'
        await ctx.send(embed=get_embed('🏓 퐁!',f'**디스코드 지연시간: **{ping}ms - {pinglevel}'))

    @commands.command(name='샤드')
    async def _shard_id(self, ctx: commands.Context):
        await ctx.send(embed=discord.Embed(description=f'**이 서버의 샤드 아이디는 `{ctx.guild.shard_id}`입니다.**', color=0xccffff))

    @commands.command(name='서버')
    async def chat_server(self, ctx):
        if ctx.author.id != 467666650183761920: return
        servers = [[s.name, len(s.members), s.owner.name] for s in self.client.guilds]
        servers.sort(key=lambda x: x[1], reverse=True)
        embed=discord.Embed(title="RT Bot 서버",description=f'총 {len(self.client.guilds)} 개의 서버', color=0xCCFFFF)
        for x in range(0,10):
            try: embed.add_field(name=s+' '+str(x+1)+'위 '+str(servers[x][0]), value="인원 : " + str(servers[x][1]) + ", 서버 주인 : " + str(servers[x][2]), inline=False)
            except: break
        await ctx.send(embed=embed)

    @commands.command(name='업타임')
    async def chat_uptime(self, ctx):
        now = datetime.datetime.utcnow()
        delta = now - start_time
        hours, remainder = divmod(int(delta.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        if days: time_format = f"**{days}**일 **{hours}**시간 **{minutes}**분  **{seconds}**초"
        else: time_format = f"**{hours}**시간 **{minutes}**분 **{seconds}**초"
        await ctx.send(f"{time_format} 동안 깨어 있었어요!")

    @commands.command(name='투표', aliases=['찬반투표', '찬반 투표'])
    async def chat_ox(self, ctx, *, arg):
        if ctx.guild is None:
            await ctx.send(embed=get_embed("<a:no:698461934613168199> | 서버내에서만 사용가능한 명령어 입니다.",0xff0000))
            return
        if arg:
            msg=await ctx.send(embed=get_embed(f'{arg}',f"By. {ctx.author.display_name}",0xCCFFFF))
            await msg.add_reaction('<a:yes:698461934198063104>')
            await msg.add_reaction('<a:no:698461934613168199>')
        else:
            await ctx.send(embed=get_embed("<a:no:698461934613168199> | 알티야 찬반투표 (내용) 의 형식으로 사용해주세요",0xff0000))

    @commands.command(name='문의', aliases=['문의해'])
    async def chat_ask(self, ctx, *, arg):
        msg=await ctx.send(embed=get_embed(f'알티봇 관리자에게 문의가 전송됩니다. ',f"문의 도배, 장난등을 치시면 알티봇 블랙리스트에 오르실수 있습니다.",0xCCFFFF))
        emjs=['<a:yes:698461934198063104>','<a:no:698461934613168199>']
        await asyncio.gather(msg.add_reaction(emjs[0]),msg.add_reaction(emjs[1]))
        def check(reaction, user):
            return user == ctx.author and msg.id == reaction.message.id and str(reaction.emoji) in emjs
        try:
            reaction, user = await self.client.wait_for('reaction_add', check=check, timeout=60)
        except asyncio.TimeoutError:
            await asyncio.gather(msg.delete(),ctx.send(embed=get_embed('⏰ | 시간이 초과되었습니다!',"", 0xFF0000)))
            return
        else:
            e = str(reaction.emoji)
            if e == '<a:yes:698461934198063104>':
                adminid=self.client.get_user(467666650183761920)
                embed=discord.Embed(title = f"{ctx.author.id} {ctx.author.name}\n서버 : {ctx.guild.name}",description=arg,color=0x00FFFF)
                await asyncio.gather(adminid.send(embed=embed),ctx.send(embed=get_embed("<a:yes:698461934198063104> | **문의 전송 완료!**")))
            elif e == '<a:no:698461934613168199>':
                await ctx.send(embed=get_embed("<a:no:698461934613168199> | 취소 되었습니다.","",0xff0000))
                return

    @commands.command(name='프로필')
    async def chat_profile(self, ctx, user: typing.Optional[discord.Member]=None):
        if ctx.guild is None:
            await ctx.send(embed=get_embed("<a:no:698461934613168199> | 서버내에서만 사용가능한 명령어 입니다.",0xff0000))
            return
        if not user: user = ctx.author
        if user.display_name == user.name: embed = discord.Embed(title=f"👤 | **{user.name} 님의 프로필**", description=f'**유저 ID** : {user.id}',color=0xCCFFFF)
        else: embed = discord.Embed(title=f"👤 | **{user.name} 님의 프로필**",description=f"닉네임 : ({user.display_name})\n**유저 ID** : {user.id}", color=0xCCFFFF)
        embed.set_thumbnail(url=user.avatar_url)
        try:
            st = str(user.status)
            if st == "online": sta = ":green_circle: 온라인"
            elif st == "offline": sta = ":black_circle: 오프라인"
            elif st == "idle": sta = ":yellow_circle: 자리 비움"
            else: sta = ":no_entry: 방해 금지"
        except: sta = "불러오는데 실패"
        embed.add_field(name="현재 상태", value=sta, inline=True)
        date = datetime.datetime.utcfromtimestamp(((int(user.id) >> 22) + 1420070400000)/1000)
        embed.add_field(name="Discord 가입 일시", value=str(date.year) + "년 " + str(date.month) + "월 " + str(date.day) + "일 ", inline=True)
        joat = user.joined_at.isoformat()
        embed.add_field(name="서버 가입 일시", value=joat[0:4]+'년 '+joat[5:7]+'월 '+joat[8:10]+'일', inline=True)
        if user.id==467666650183761920: embed.add_field(name="봇 권한", value="ADMIN", inline=True)
        elif user.id==473371560703557653 or user.id==315467368656666635: embed.add_field(name="봇 권한", value="BETA TESTER", inline=True)
        else : embed.add_field(name="봇 권한", value="USER", inline=True)
        if user.guild_permissions.administrator: embed.add_field(name="서버 권한", value="ADMIN", inline=True)
        else: embed.add_field(name="서버 권한", value="USER", inline=True)
        if str(user.id) in emblem.keys(): embed.add_field(name="칭호", value="\n".join(emblem[str(user.id)]), inline=True)
        await ctx.send(embed=embed)

    @commands.group(name='칭호')
    async def _emblem(self, ctx):
        pass

    @_emblem.command(name='추가')
    async def _emblem_add(self, ctx):
        pass

    @_emblem.command(name='삭제')
    async def _emblem_erase(self, ctx):
        pass

    @commands.command(name='프사')
    async def chat_profile_image(self, ctx, user: typing.Optional[discord.Member]=None):
        if not user: user = ctx.author
        await ctx.send(embed=get_embed(f"<:image_icon:712928351949684788> | {user.name} 님의 프로필사진", color=0xccffff).set_image(url=user.avatar_url))

    @commands.command(name='초대장')
    async def chat_cheowkd(self, ctx):
        await ctx.send(embed=get_embed("📋 | 알티봇 초대",">>> [알티봇 다른서버에 초대하기!](https://discordapp.com/api/oauth2/authorize?client_id=661477460390707201&permissions=8&scope=bot)\n\n[알티봇 서포트 서버!](https://discord.gg/hTZxtbC)"))

def setup(client):
    client.add_cog(chat(client))
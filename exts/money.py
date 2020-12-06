import discord, json, asyncio, typing
import traceback
from discord.ext import commands, tasks
from random import randint
from utils import errors

with open("./data/userdatabase.json", "r", encoding='UTF8') as db_json: userdb = json.load(db_json)
with open("./data/lotto.json", "r", encoding='UTF8') as db_json: lottodb = json.load(db_json)
with open("./data/reinforce.json","r", encoding='UTF-8') as db_json: rfdb = json.load(db_json)

def get_embed(title, description='', color=0xCCFFFF): 
    return discord.Embed(title=title,description=description,color=color)

class money(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.gaming_list = []
        self.tictactoe = {}

    @commands.group(name='가위바위보', invoke_without_command=True)
    async def rsp(self,ctx):
        await ctx.send(embed=get_embed("가위바위보 빠, 가위바위보 묵, 가위바위보 찌 셋중 하나를 골라서 해주세요"))
    
    @rsp.command(name="보",aliases=["빠"])
    async def rsp_bo(self,ctx):
        if str(ctx.author.id) not in userdb.keys():
            await ctx.send(embed=get_embed('<a:no:698461934613168199> | 가입 되어 있지 않습니다!',"<알티야 가입> 으로 가입해주세요", 0xFF0000))
            return
        emjs=['✋','✌️','✊']
        botsay=randint(0,2)
        await ctx.send(f"당신의 선택 : ✋\n봇의 선택 : {emjs[botsay]}")
        n = randint(1000,10000)
        if botsay == 0: 
            await ctx.send("비겼습니다!")
        elif botsay == 1: 
            await ctx.send(f"졌습니다ㅠㅠ\n{n}원 잃음")
            userdb[str(ctx.author.id)]["money"] = userdb[str(ctx.author.id)]["money"] - n
        elif botsay == 2: 
            await ctx.send(f"이겼습니다!\n{n}원 획득!")
            userdb[str(ctx.author.id)]["money"] = userdb[str(ctx.author.id)]["money"] + n

    @rsp.command(name="찌",aliases=["가위"])
    async def rsp_sissors(self,ctx):
        if str(ctx.author.id) not in userdb.keys():
            await ctx.send(embed=get_embed('<a:no:698461934613168199> | 가입 되어 있지 않습니다!',"<알티야 가입> 으로 가입해주세요", 0xFF0000))
            return
        emjs=['✋','✌️','✊']
        botsay=randint(0,2)
        await ctx.send(f"당신의 선택 : ✌️\n봇의 선택 : {emjs[botsay]}")
        n = randint(1000,10000)
        if botsay == 1: 
            await ctx.send("비겼습니다!")
        elif botsay == 2: 
            await ctx.send(f"졌습니다ㅠㅠ\n{n}원 잃음")
            userdb[str(ctx.author.id)]["money"] = userdb[str(ctx.author.id)]["money"] - n
        elif botsay == 0: 
            await ctx.send(f"이겼습니다!\n{n}원 획득!")
            userdb[str(ctx.author.id)]["money"] = userdb[str(ctx.author.id)]["money"] + n

    @rsp.command(name="묵",aliases=["바위"])
    async def rsp_rocks(self,ctx):
        if str(ctx.author.id) not in userdb.keys():
            await ctx.send(embed=get_embed('<a:no:698461934613168199> | 가입 되어 있지 않습니다!',"<알티야 가입> 으로 가입해주세요", 0xFF0000))
            return
        emjs=['✋','✌️','✊']
        botsay=randint(0,2)
        await ctx.send(f"당신의 선택 : ✊\n봇의 선택 : {emjs[botsay]}")
        n = randint(1000,10000)
        if botsay == 2: 
            await ctx.send("비겼습니다!")
        elif botsay == 0: 
            await ctx.send(f"졌습니다ㅠㅠ\n{n}원 잃음")
            userdb[str(ctx.author.id)]["money"] = userdb[str(ctx.author.id)]["money"] - n
        elif botsay == 1: 
            await ctx.send(f"이겼습니다!\n{n}원 획득!")
            userdb[str(ctx.author.id)]["money"] = userdb[str(ctx.author.id)]["money"] + n

    @commands.group(name='강화', aliases=['강'], invoke_without_command=True)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def _reinforce(self, ctx, *, weapon):
        if str(ctx.author.id) not in userdb.keys(): 
            await ctx.send(embed=get_embed('<a:no:698461934613168199> | 가입 되어 있지 않습니다!',"<알티야 가입> 으로 가입해주세요", 0xFF0000))
            return
        user = str(ctx.author.id)
        if not weapon:
            await ctx.send("알티야 강화 (이름)의 형식으로 사용해주세용")
            return
        if user not in rfdb.keys(): rfdb[user] = {}
        if weapon not in rfdb[user].keys(): 
            if len(rfdb[user]) >= 20:
                await ctx.send(embed=get_embed('<a:no:698461934613168199> | 강화는 최대 20개까지 가능합니다.',"<알티야 강화 삭제 (이름)> 또는 <알티야 강화 판매 (이름)>으로 강화 수를 줄여주세요", 0xFF0000))
                return
            else: rfdb[user][weapon]=0
        if rfdb[user][weapon] >= 100:
            msg = await ctx.send(embed=get_embed(":hammer: | 특수 강화","100렙을 넘으셔서 특수강화 도전을 하실수 있습니다.\n성공 : 50% (5~20 레벨 랜덤 오름)\n실패 : 50% (실패시 80레벨로 복구)\n도전 하시겠습니까?"))
            emjs=['<a:yes:698461934198063104>','<a:no:698461934613168199>']
            await msg.add_reaction(emjs[0])
            await msg.add_reaction(emjs[1])
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
                    if randint(1,101) > 50:
                        user = str(ctx.author.id)
                        f = randint(5,20)
                        rfdb[user][weapon]=int(rfdb[user][weapon])+f
                        await ctx.send(embed=get_embed(f"<a:yes:698461934198063104> | {weapon} (이)가 **{f}레벨** 성장했습니다.",f"현재 레벨 : **{rfdb[user][weapon]}**"))
                        return
                    else:
                        user = str(ctx.author.id)
                        rfdb[user][weapon] = 80
                        await ctx.send(embed=get_embed(f"<a:no:698461934613168199> | {weapon} (이)가 파괴되었습니다.","",0xff0000))
                        return
                elif e == '<a:no:698461934613168199>':
                    await ctx.send(embed=get_embed("<a:no:698461934613168199> | 취소 되었습니다.","",0xff0000))
                    return
        else:
            s=int(rfdb[user][weapon])
            if randint(1,105) > s:
                n = randint(2,10)
                rfdb[user][weapon]=s+n
                await ctx.send(f"**성공!** {weapon} (이)가 **{105-s}%**의 확률로 **{n}레벨** 성장했습니다\n현재 레벨 : **{rfdb[user][weapon]}**")
            else: 
                n=randint(1,5)
                rfdb[user][weapon]=s-n
                await ctx.send(f"**실패..** {weapon}이가 **{5+s}%**의 확률로 **{n}레벨** 하강ㅠㅠ\n현재 레벨 : **{rfdb[user][weapon]}**")
            with open("./data/reinforce.json", "w", encoding='utf-8') as database_json: database_json.write(json.dumps(rfdb, ensure_ascii=False, indent=4))

    @_reinforce.command(name='관리자_강화설정')
    async def _rf_admin_set_rf(self, ctx, *, arg):
        if ctx.author.id != 467666650183761920: return
        rfdb[arg.split(" ")[0]][arg.split(" ")[1]] = int(arg.split(" ")[2])
        await ctx.send(f'id={arg.split(" ")[0]} name={arg.split(" ")[1]} Lv = {arg.split(" ")[2]}')
                
    @_reinforce.command(name='목록', aliases=['물품','리스트'])
    async def _rf_list(self, ctx):
        if str(ctx.author.id) not in userdb.keys():
            await ctx.send(embed=get_embed('<a:no:698461934613168199> | 가입 되어 있지 않습니다!',"<알티야 가입> 으로 가입해주세요", 0xFF0000))
            return
        if str(ctx.author.id) not in rfdb.keys():
            await ctx.send(embed=get_embed("<a:no:698461934613168199> | 강화한 물품이 없습니다","",0xff0000))
            return
        lis = []
        for s in rfdb[str(ctx.author.id)]:
            lis.append("**Lv" + str(rfdb[str(ctx.author.id)][s])+"**  " + s)
        await ctx.send(embed=get_embed(f":wrench: **{ctx.author} 님의 강화 목록**","\n".join(lis)))

    @_reinforce.command(name='삭제')
    async def _rf_erase(self, ctx, *, arg):
        if str(ctx.author.id) not in userdb.keys():
            await ctx.send(embed=get_embed('<a:no:698461934613168199> | 가입 되어 있지 않습니다!',"<알티야 가입> 으로 가입해주세요", 0xFF0000))
            return
        if str(ctx.author.id) not in rfdb.keys():
            await ctx.send(embed=get_embed("<a:no:698461934613168199> | 강화한 물품이 없습니다","",0xff0000))
            return
        if arg not in rfdb[str(ctx.author.id)].keys():
            await ctx.send(embed=get_embed("<a:no:698461934613168199> | 찾을수 없는 물품입니다.","",0xff0000))
            return
        level = rfdb[str(ctx.author.id)][arg]
        msg  = await ctx.send(embed=get_embed("📄 | 강화 삭제",f"**Lv.{level} {arg}**\n\n정말 삭제 하시겠습니까?"))
        emjs=['<a:yes:698461934198063104>','<a:no:698461934613168199>']
        await msg.add_reaction(emjs[0])
        await msg.add_reaction(emjs[1])
        def check(reaction, user):
            return user == ctx.author and msg.id == reaction.message.id and str(reaction.emoji) in emjs
        try:
            reaction, user = await self.client.wait_for('reaction_add', check=check, timeout=60)
        except asyncio.TimeoutError:
            await asyncio.gather(
                msg.delete(),
                ctx.send(embed=get_embed('⏰ | 시간이 초과되었습니다!',"", 0xFF0000))
                )
            return
        else:
            e = str(reaction.emoji)
            if e == '<a:yes:698461934198063104>':
                del rfdb[str(ctx.author.id)][arg]
                await ctx.send(embed=get_embed("<a:yes:698461934198063104> | 삭제 완료!"))
                with open("./data/reinforce.json", "w", encoding='utf-8') as database_json: database_json.write(json.dumps(rfdb, ensure_ascii=False, indent=4))
                return
            elif e == '<a:no:698461934613168199>':
                await ctx.send(embed=get_embed("<a:no:698461934613168199> | 취소 되었습니다.","",0xff0000))
                return

    @_reinforce.command(name='판매')
    async def _rf_sell(self, ctx, *, arg):
        if str(ctx.author.id) not in userdb.keys():
            await ctx.send(embed=get_embed('<a:no:698461934613168199> | 가입 되어 있지 않습니다!',"<알티야 가입> 으로 가입해주세요", 0xFF0000))
            return
        if str(ctx.author.id) not in rfdb.keys():
            await ctx.send(embed=get_embed("<a:no:698461934613168199> | 강화한 물품이 없습니다","",0xff0000))
            return
        if arg not in rfdb[str(ctx.author.id)].keys():
            await ctx.send(embed=get_embed("<a:no:698461934613168199> | 찾을수 없는 물품입니다.","",0xff0000))
            return
        level = rfdb[str(ctx.author.id)][arg]
        if level < 60:
            await ctx.send(embed=get_embed("<a:no:698461934613168199> | 60레벨 이상의 물품만 판매하실수 있습니다.","<알티야 강화 삭제> 명령어로 삭제가 가능합니다.",0xff0000))
            return
        n = round(2**(round(1.2**(level/4))))
        msg  = await ctx.send(embed=get_embed("📄 | 강화 판매",f"**Lv.{level} {arg}**\n\n의 가치는 {n}입니다.\n정말 판매 하시겠습니까?"))
        emjs=['<a:yes:698461934198063104>','<a:no:698461934613168199>']
        await msg.add_reaction(emjs[0])
        await msg.add_reaction(emjs[1])
        def check(reaction, user):
            return user == ctx.author and msg.id == reaction.message.id and str(reaction.emoji) in emjs
        try:
            reaction, user = await self.client.wait_for('reaction_add', check=check, timeout=60)
        except asyncio.TimeoutError:
            await asyncio.gather(
                msg.delete(),
                ctx.send(embed=get_embed('⏰ | 시간이 초과되었습니다!',"", 0xFF0000))
                )
            return
        else:
            e = str(reaction.emoji)
            if e == '<a:yes:698461934198063104>':
                del rfdb[str(ctx.author.id)][arg]
                userdb[str(user.id)]["money"] = userdb[str(user.id)]["money"] + n
                await ctx.send(embed=get_embed("<a:yes:698461934198063104> | 판매 완료!",f'{n}원이 지급되었습니다.\n\n**현재 소지금**\n{userdb[str(user.id)]["money"]}'))
                with open("./data/reinforce.json", "w", encoding='utf-8') as database_json: database_json.write(json.dumps(rfdb, ensure_ascii=False, indent=4))
                with open("./data/userdatabase.json", "w", encoding='utf-8') as database_json: database_json.write(json.dumps(userdb, ensure_ascii=False, indent=4))
                return
            elif e == '<a:no:698461934613168199>':
                await ctx.send(embed=get_embed("<a:no:698461934613168199> | 취소 되었습니다.","",0xff0000))
                return

    @_reinforce.group(name='순위', invoke_without_command=True)
    async def _rf_rank(self, ctx):
        await ctx.send(embed=get_embed("<a:no:698461934613168199> | 올바르지 않은 명령어입니다!","알티야 강화 순위 서버/전체로 사용해주세요",0xff0000))

    @_rf_rank.command(name='서버')
    async def _rf_list_server(self, ctx):
        if str(ctx.author.id) not in userdb.keys():
            await ctx.send(embed=get_embed('<a:no:698461934613168199> | 가입 되어 있지 않습니다!',"<알티야 가입> 으로 가입해주세요", 0xFF0000))
            return
        lis=[]
        for r in rfdb.keys():
            try: user = ctx.guild.get_member(int(r)).name
            except: pass
            else:
                for s in rfdb[r]: 
                    lis.append([user, s, rfdb[r][s]])
        lis.sort(key=lambda x: x[2], reverse=True)
        embed=get_embed(":bar_chart: | 서버 강화 순위 TOP6")
        alis = []
        a=0
        for r in lis:
            if a ==0: medal = '<:LeaderboardTrophy01:716106586333904986>'
            elif a==1: medal = '<:silverthropy:736215959823712306>'
            elif a==2: medal = '<:bronzethropy:736215949614645269>'
            else: medal = '🏅'
            alis.append(f"{medal} | **{r[0]}**\n> **Lv{r[2]}** {r[1]}\n\n")
            a+=1
            if a>=6: break
        await ctx.send(embed=get_embed(":bar_chart: | 서버 강화 순위","".join(alis)))

    @_rf_rank.command(name='전체')
    async def _rf_list_all(self, ctx):
        if str(ctx.author.id) not in userdb.keys():
            await ctx.send(embed=get_embed('<a:no:698461934613168199> | 가입 되어 있지 않습니다!',"<알티야 가입> 으로 가입해주세요", 0xFF0000))
            return
        lis=[]
        for r in rfdb.keys():
            try: user = self.client.get_user(int(r)).name
            except: user = int(r)
            else:
                for s in rfdb[r]: lis.append([user, s, rfdb[r][s]])
        lis.sort(key=lambda x: x[2], reverse=True)
        embed=get_embed(":bar_chart: | 알티봇 강화 순위 TOP6")
        alis = []
        a=0
        for r in lis:
            if a ==0: medal = '<:LeaderboardTrophy01:716106586333904986>'
            elif a==1: medal = '<:silverthropy:736215959823712306>'
            elif a==2: medal = '<:bronzethropy:736215949614645269>'
            else: medal = '🏅'
            alis.append(f"{medal} | **{r[0]}**\n**Lv{r[2]}** {r[1]}\n\n")
            a+=1
            if a>=6: break
        await ctx.send(embed=get_embed(":bar_chart: | 서버 강화 순위","".join(alis)))

    @commands.command(name="숫자맞추기", aliases=['숫맞','업다운','업다운게임'])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def updown(self, ctx, n: typing.Union[str, int, None] = None):
        if str(ctx.author.id) not in userdb.keys():
            await ctx.send(embed=get_embed('<a:no:698461934613168199> | 가입 되어 있지 않습니다!',"<알티야 가입> 으로 가입해주세요", 0xFF0000))
            return
        if ctx.author.id in self.gaming_list:
            await ctx.send(embed=get_embed("<a:no:698461934613168199> | 이미 다른 게임이 진행중입니다.", "",0xff0000))
            return
                                               
        self.gaming_list.append(ctx.author.id)
        money = userdb[str(ctx.author.id)]["money"]
                                               
        if not n:
            await ctx.send(embed=get_embed("💵 | 거실금액을 입력해주세요"))

            def check(author):
                def inner_check(message): 
                    if message.author != author: return False
                    else: return True
                return inner_check
            try: msg = await self.client.wait_for('message',check=check(ctx.author),timeout=20)
            except asyncio.TimeoutError: 
                self.gaming_list.remove(ctx.author.id)
                await ctx.send(embed=get_embed('⏰ | 시간이 초과되었습니다!',"", 0xFF0000))
                return
            else: 
                n = msg.content
                if n in ["0","X","x"]:
                    self.gaming_list.remove(ctx.author.id)
                    await ctx.send(embed=get_embed("<a:no:698461934613168199> | 취소 되었습니다.","",0xff0000))
                    return

        try: int(n)
        except:
            if n in ["올인","전부","전체","최대"]: n=money
            else: 
                self.gaming_list.remove(ctx.author.id)
                raise errors.morethan1
        else: n = int(n)

        if n < 0: 
            self.gaming_list.remove(ctx.author.id)
            raise errors.morethan1

        if n > money: 
            self.gaming_list.remove(ctx.author.id)
            raise errors.NoMoney
                                               
        embed=get_embed("⚖️ | 숫자맞추기 난이도를 정해주세요","실패시 걸은돈은 삭제됩니다.")
        embed.add_field(name="😀 | 쉬움",value="1~10까지의 수중 뽑습니다.\n보상 : 걸은돈의 1 ~ 2배")
        embed.add_field(name="😠 | 보통",value="1~20까지의 수중 뽑습니다.\n보상 : 걸은돈의 2 ~ 4배")
        embed.add_field(name="🤬 | 어려움",value="1~30까지의 수중 뽑습니다.\n보상 : 걸은돈의 3 ~ 6배")
        embed.set_footer(text="❌를 눌러 취소")
        msg = await ctx.send(embed=embed)
                                               
        number = 0
        lev = 0                   
                                               
        emjs=['😀','😠','🤬','❌']
        for em in emjs: await msg.add_reaction(em)
                                               
        def check(reaction, user):
            return user == ctx.author and msg.id == reaction.message.id and str(reaction.emoji) in emjs
        try: reaction, user = await self.client.wait_for('reaction_add', check=check, timeout=60)
        except asyncio.TimeoutError:
            await asyncio.gather(msg.delete(),ctx.send(embed=get_embed('⏰ | 시간이 초과되었습니다!',"", 0xFF0000)))
            self.gaming_list.remove(ctx.author.id)
            return
        else:
            e = str(reaction.emoji)
            if e == '😀':
                number = randint(1,10)
                lev = 1
            elif e == '😠':
                number = randint(1,20)
                lev = 2
            elif e == '🤬':
                number = randint(1,30)
                lev = 3
            elif e == '❌':
                self.gaming_list.remove(ctx.author.id)
                await ctx.send(embed=get_embed("<a:no:698461934613168199> | 취소 되었습니다.","",0xff0000))
                return
                                               
        await ctx.send(embed=get_embed('입력해주세요'))
                                               
        def check(author):
            def inner_check(message): 
                if message.author != author: return False
                try: int(message.content) 
                except ValueError: return False
                else: return True
            return inner_check
        try: msg = await self.client.wait_for('message',check=check(ctx.author),timeout=30)
        except asyncio.TimeoutError: 
            await ctx.send(embed=get_embed('⏰ | 시간이 초과되었습니다!',"", 0xFF0000))
            self.gaming_list.remove(ctx.author.id)
            return

        userdb[str(ctx.author.id)]["money"] = userdb[str(ctx.author.id)]["money"] - n
        attempt = abs(int(msg.content)-number)
        if attempt == 0:
            lev = lev * 2
            await ctx.send(f'정확합니다!! 원래 숫자는 {number}였습니다. **({lev}배)**\n{n*lev} 원 지급!')
        elif attempt == 1:
            lev = lev * 1.5
            await ctx.send(f'1차이! 원래 숫자는 {number}였습니다. **({lev}배)**\n{int(n*lev)} 원 지급!')
        elif attempt == 2:
            await ctx.send(f'2차이~ 원래 숫자는 {number}였습니다. **({lev}배)**\n{n*lev} 원 지급!')
        else:
            await ctx.send(f'맞추지 못했습니다...')
            self.gaming_list.remove(ctx.author.id)
            return
        userdb[str(ctx.author.id)]["money"] = money + int(n*lev)
        self.gaming_list.remove(ctx.author.id)
        return

    @commands.command(name="슬롯")
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def slot(self, ctx, arg):
        user = str(ctx.author.id)
        money=int(userdb[user]["money"])
        if arg == '최대': arg=money//200
        else: arg=int(arg)
        if user not in userdb.keys(): raise errors.morethan1
        if ctx.author.id in self.gaming_list:
            await ctx.send(embed=get_embed("<a:no:698461934613168199> | 이미 다른 게임이 진행중입니다.", "",0xff0000))
            return
        if money < 2000: 
            await ctx.send(embed=get_embed("<a:no:698461934613168199> | 최소 2000원의 자산이 있어야 가능합니다.", f"현재 금액 : {money}",0xff0000))
            return
        if arg > money: raise errors.NoMoney
        if arg <= 0: raise errors.morethan1
        maxmoney = money//200
        if arg > maxmoney:
            await ctx.send(embed=get_embed("<a:no:698461934613168199> | 현재 금액의 200분의 1 이상 사용불가합니다.", f"최대사용금액 : {maxmoney}",0xff0000))
            return
        self.gaming_list.append(ctx.author.id)
        allslot = ['🔔','⭐','🍒','🍈','❌','💩']
        slotbae = [10,6,2,0,-1,-2]
        msg=await ctx.send(embed=get_embed("🎰 | 슬롯","🔔 **10** \n⭐ **6** \n🍒 **2** \n🍈 **0** \n❌ **-1** \n💩 **-2** \n\n참여 하시겠습니까?"))
        emjs=['<a:yes:698461934198063104>','<a:no:698461934613168199>']
        for em in emjs: await msg.add_reaction(em)
        def check(reaction, user):
            return user == ctx.author and msg.id == reaction.message.id and str(reaction.emoji) in emjs
        try:
            reaction, user = await self.client.wait_for('reaction_add', check=check, timeout=20)
        except asyncio.TimeoutError:
            await asyncio.gather(
                msg.delete(),
                ctx.send(embed=get_embed('⏰ | 시간이 초과되었습니다!',"", 0xFF0000))
                )
        else:
            e = str(reaction.emoji)
            if e == '<a:yes:698461934198063104>':
                msg1=await ctx.send("❓ ❓ ❓")
                await asyncio.sleep(5)
                slot=[randint(0,5),randint(0,5),randint(0,5)]
                await msg1.edit(content=f"❓ ❓ {allslot[slot[0]]}")
                await asyncio.sleep(2)
                await msg1.edit(content=f"❓ {allslot[slot[1]]} {allslot[slot[0]]}")
                await asyncio.sleep(2)
                await msg1.edit(content=f"{allslot[slot[2]]} {allslot[slot[1]]} {allslot[slot[0]]}")
                bae = 1
                for a in slot:
                    bae=bae * slotbae[a]
                await ctx.send(f"총 배수 = {bae}")
                userdb[str(ctx.author.id)]["money"]=money + (arg*bae)
                with open("./data/userdatabase.json", "w", encoding='utf-8') as database_json: database_json.write(json.dumps(userdb, ensure_ascii=False, indent=4))
                self.gaming_list.remove(ctx.author.id)
                return
            elif e == '<a:no:698461934613168199>':
                await asyncio.gather(
                    msg.delete(),
                    ctx.send(embed=get_embed('<a:no:698461934613168199> | 취소 되었습니다!',"", 0xFF0000))
                )
                self.gaming_list.remove(ctx.author.id)
                return
        self.gaming_list.remove(ctx.author.id)
        return

    @commands.command(name="유저", aliases=['유'])
    async def now_playing_user(self, ctx):
        embed = get_embed("🎮 | 게임 유저",f"현재 알티봇을 플레이하고 있는 유저는 {len(self.gaming_list)}명입니다\n\n알티봇의 가입자 수는 {len(userdb)}명 서버는 {len(self.client.guilds)}개 입니다")
        embed.set_thumbnail(url=self.client.user.avatar_url)
        await ctx.send(embed=embed)
    
    @commands.command(name='로또')
    async def _lotto(self, ctx):
        if str(ctx.author.id) not in userdb.keys():
            await ctx.send(embed=get_embed('<a:no:698461934613168199> | 가입 되어 있지 않습니다!',"<알티야 가입> 으로 가입해주세요", 0xFF0000))
            return
        if str(ctx.author.id) in lottodb.keys():
            await ctx.send(embed=get_embed("<a:no:698461934613168199> | 이미 참여 하셨습니다","",0xff0000))
            return
        msg = await ctx.send(embed=get_embed("제1차 알티봇 로또","매주 일요일 결과가 공개 됩니다.\n\n참여 하시겠습니까?"))
        emjs=['<a:yes:698461934198063104>','<a:no:698461934613168199>']
        for em in emjs: await msg.add_reaction(em)
        def check(reaction, user):
            return user == ctx.author and msg.id == reaction.message.id and str(reaction.emoji) in emjs
        try:
            reaction, user = await self.client.wait_for('reaction_add', check=check, timeout=20)
        except asyncio.TimeoutError:
            await asyncio.gather(
                msg.delete(),
                ctx.send(embed=get_embed('⏰ | 시간이 초과되었습니다!',"", 0xFF0000))
                )
            return
        else:
            e = str(reaction.emoji)
            if e == '<a:yes:698461934198063104>':
                pickmsg = await ctx.send(embed=get_embed("1~100중에서 수를 골라주세요!","일치하는 수가 1등, ±1이 2등 ±2가 3등입니다.\n보상은 항상 바뀝니다"))
                def check(m):
                    return m.author == ctx.author and m.channel == ctx.channel and m.content
                try:
                    m = await self.client.wait_for('message', check=check, timeout=60)
                except asyncio.TimeoutError:
                    await ctx.send(embed=discord.Embed(title='⏰ 시간이 초과되었습니다!', color=0xff0000))
                else:
                    try:
                        picknum = int(m.content)
                    except:
                        await ctx.send(embed=get_embed("<a:no:698461934613168199> | 정수값을 적어주세요"))
                    else:
                        if not (0<=picknum<=100):
                            await ctx.send(embed=get_embed("<a:no:698461934613168199> | 0이상 100이하의 수를 적어주세요."))
                            return
                        lottodb[str(ctx.author.id)] = picknum
                        await ctx.send(embed=get_embed(f"<a:yes:698461934198063104> | 로또가 접수 되었습니다",f"NAME : **{ctx.author}**\nUSERID : **{ctx.author.id}**\nNUM : **{picknum}**"))
                        with open("./data/lotto.json", "w", encoding='utf-8') as database_json:
                            database_json.write(json.dumps(lottodb, ensure_ascii=False, indent=4))
            elif e == '<a:no:698461934613168199>':
                await asyncio.gather(
                    msg.delete(),
                    ctx.send(embed=get_embed('<a:no:698461934613168199> | 취소 되었습니다!',"", 0xFF0000))
                )

    @commands.group(name='도박', invoke_without_command=True)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def _dobak(self, ctx, n:int):
            if str(ctx.author.id) not in userdb.keys():
                await ctx.send(embed=get_embed('<a:no:698461934613168199> | 가입 되어 있지 않습니다!',"<알티야 가입> 으로 가입해주세요", 0xFF0000))
                return
            user = str(ctx.author.id)
            money=int(userdb[user]["money"])
            rand = randint(0, 100)
            if money < n: raise errors.NoMoney
            if n < 1: raise errors.morethan1
            if rand <= 11:
                await ctx.send('-1배ㅋㅋㅋㅋㅋ')
                n = n * -2
                if money + n < 0:  userdb[user]["money"] = 0
                else: userdb[user]["money"] = money + n
            elif rand <= 31:
                await ctx.send('0배 ㅋ')
            elif rand <= 81:
                await ctx.send('1배!')
                userdb[user]["money"] = money + n
            else:
                await ctx.send('2배!!')
                userdb[user]["money"] = 2 * n + money
            with open("./data/userdatabase.json", "w", encoding='utf-8') as database_json: database_json.write(json.dumps(userdb, ensure_ascii=False, indent=4))

    @_dobak.command(name='전체', aliases=['올인','올'])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def dobak_all(self, ctx):
        if str(ctx.author.id) not in userdb.keys():
            await ctx.send(embed=get_embed('<a:no:698461934613168199> | 가입 되어 있지 않습니다!',"<알티야 가입> 으로 가입해주세요", 0xFF0000))
            return
        user = str(ctx.author.id)
        money=int(userdb[user]["money"])
        rand = randint(0, 100)
        if money <= 0:
            await ctx.send(embed=get_embed('<a:no:698461934613168199> | 돈이 부족합니다!','',0xff0000))
            return
        if rand <= 15:
            await ctx.send("0배 ㅋ")
            userdb[user]["money"] = 0
        elif rand <= 20:
            await ctx.send("0.01배 ㅋㅋㅋㅋㅋㅋㅋㅋ")
            userdb[user]["money"] = userdb[user]["money"] // 100
        elif rand <= 40:
            await ctx.send("0.1배 ㅋㅋㅋㅋ")
            userdb[user]["money"] = userdb[user]["money"] // 10
        elif rand <= 60:
            await ctx.send("0.5배 ㅋㅋㅋㅋ")
            userdb[user]["money"] = userdb[user]["money"] // 2
        elif rand <= 65:
            await ctx.send("2배!!")
            userdb[user]["money"] = userdb[user]["money"] * 2
        elif rand <= 75:
            await ctx.send("4배!!!")
            userdb[user]["money"] = userdb[user]["money"] * 4
        elif rand <= 80:
            await ctx.send("5배!!!")
            userdb[user]["money"] = userdb[user]["money"] * 5
        elif rand <= 88:
            await ctx.send("10배!!!!!!")
            userdb[user]["money"] = userdb[user]["money"] * 10
        elif rand <= 98:
            await ctx.send("20배!!!!!!!")
            userdb[user]["money"] = userdb[user]["money"] * 20
        elif rand <= 99:
            await ctx.send("50배!!!!!!!!")
            userdb[user]["money"] = userdb[user]["money"] * 50
        elif rand <= 100:
            await ctx.send("100배!!!!!!!!")
            userdb[user]["money"] = userdb[user]["money"] * 100
        with open("./data/userdatabase.json", "w", encoding='utf-8') as database_json: database_json.write(json.dumps(userdb, ensure_ascii=False, indent=4))

    @commands.command(name='돈내놔', aliases=['돈줘','돈받기',"ㄷㅂㄱ"])
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def _give_me_money(self, ctx):
        if str(ctx.author.id) not in userdb: 
            await ctx.send(embed=get_embed('<a:no:698461934613168199> | 가입 되어 있지 않습니다!',"<알티야 가입> 으로 가입해주세요", 0xFF0000))
            return
        userdb[str(ctx.author.id)]["money"] = userdb[str(ctx.author.id)]["money"] + 400
        await ctx.send("400원 지급 완료!")
        with open("./data/userdatabase.json", "w", encoding='utf-8') as database_json:
                database_json.write(json.dumps(userdb, ensure_ascii=False, indent=4))

    @commands.group(name='내돈', aliases=['지갑','돈',"니돈","ㄴㄷ","ㄷ"], invoke_without_command=True)
    async def _mymoney(self, ctx, user: typing.Optional[discord.Member]=None):
        if str(ctx.author.id) not in userdb: 
            await ctx.send(embed=get_embed('<a:no:698461934613168199> | 가입 되어 있지 않습니다!',"<알티야 가입> 으로 가입해주세요", 0xFF0000))
            return
        if user:
            if str(user.id) not in userdb:
                await ctx.send(embed=get_embed('<a:no:698461934613168199> | 가입 되어 있지 않은 유저입니다!',"<알티야 가입> 으로 가입해주세요", 0xFF0000))
                return
        else: 
            user = ctx.author
        money=userdb[str(user.id)]["money"]
        await ctx.send(embed=get_embed(f'💸 | {user} 님의 지갑',f"{money} 원"))

    @_mymoney.command(name="한글")
    async def _mymoney_kor(self, ctx, user: typing.Optional[discord.Member]=None):
        if str(ctx.author.id) not in userdb: 
            await ctx.send(embed=get_embed('<a:no:698461934613168199> | 가입 되어 있지 않습니다!',"<알티야 가입> 으로 가입해주세요", 0xFF0000))
            return
        if user:
            if str(user.id) not in userdb:
                await ctx.send(embed=get_embed('<a:no:698461934613168199> | 가입 되어 있지 않은 유저입니다!',"<알티야 가입> 으로 가입해주세요", 0xFF0000))
                return
        else: 
            user = ctx.author

        suffix=['','만', '억', '조', '경', '해', '자', '양', '구', '간', '정', '재', '극','항하사','아승기','나유타','불가사의','무량대수','','','','','','','','구골','','','','','','','','','','','','','','','','','','','','','','','','']
        a=10000 ** 50
        money=userdb[str(user.id)]["money"]
        if money > a: 
            await ctx.send(embed=get_embed("<a:no:698461934613168199> | 수가 너무 커서 계산이 불가합니다","구골^2 이상",0xff0000))
            return
        str_result = ''
        for i in range(0,51):
            if money >= a:
                str_result += f"{int(money // a)}{suffix[-i]} "
                money = money % a
            a=a//10000

        await ctx.send(embed=get_embed(f'💸 | {user} 님의 지갑',f"{str_result.strip()} 원"))

    @commands.command(name='탈퇴')
    async def _logout(self, ctx):
        if str(ctx.author.id) not in userdb: 
            await ctx.send(embed=get_embed('<a:no:698461934613168199> | 가입 되어 있지 않습니다!',"<알티야 가입> 으로 가입해주세요", 0xFF0000))
            return
        msg = await ctx.send(embed=get_embed("📝 | **알티봇 서비스에서 탈퇴하시겠습니까?**","탈퇴시, 돈과 강화 목록을 포함한 모든 데이터가 영구적으로 삭제되며 복구할수 없습니다."))
        emjs=['<a:yes:698461934198063104>','<a:no:698461934613168199>']
        for em in emjs: await msg.add_reaction(em)
        def check(reaction, user):
            return user == ctx.author and msg.id == reaction.message.id and str(reaction.emoji) in emjs
        try:
            reaction, user = await self.client.wait_for('reaction_add', check=check, timeout=20)
        except asyncio.TimeoutError:
            await asyncio.gather(msg.delete(),ctx.send(embed=get_embed('⏰ | 시간이 초과되었습니다!',"", 0xFF0000)))
            return
        else:
            e = str(reaction.emoji)
            if e == '<a:yes:698461934198063104>':
                del userdb[str(ctx.author.id)]
                await asyncio.gather(msg.delete(),ctx.send(embed=get_embed('<a:yes:698461934198063104> | 탈퇴에 성공했습니다!',"", 0xCCFFFF)))
                return
            elif e == '<a:no:698461934613168199>':
                await asyncio.gather(msg.delete(),ctx.send(embed=get_embed('<a:no:698461934613168199> | 취소 되었습니다!',"", 0xFF0000)))
                return
                                               
    @commands.command(name='가입', aliases=['나도'])
    async def _login(self, ctx):
        if str(ctx.author.id) in userdb: 
            await ctx.send(embed=get_embed('<a:no:698461934613168199> | 이미 가입 되어 있습니다!',"", 0xFF0000))
            return
        msg = await ctx.send(embed=get_embed("📝 | **알티봇 서비스에 가입하시겠습니까?**",f"**NAME** = {ctx.author}\n**ID** = {ctx.author.id}"))
        emjs=['<a:yes:698461934198063104>','<a:no:698461934613168199>']
        for em in emjs: await msg.add_reaction(em)
        def check(reaction, user):
            return user == ctx.author and msg.id == reaction.message.id and str(reaction.emoji) in emjs
        try:
            reaction, user = await self.client.wait_for('reaction_add', check=check, timeout=20)
        except asyncio.TimeoutError:
            await asyncio.gather(msg.delete(),ctx.send(embed=get_embed('⏰ | 시간이 초과되었습니다!',"", 0xFF0000)))
            return
        else:
            e = str(reaction.emoji)
            if e == '<a:yes:698461934198063104>':
                userdb[str(ctx.author.id)] = {"money":5000,"bank":0}
                await asyncio.gather(
                    msg.delete(),
                    ctx.send(embed=get_embed('<a:yes:698461934198063104> | 가입에 성공했습니다!',"", 0xCCFFFF))
                )
                with open("./data/userdatabase.json", "w", encoding='utf-8') as database_json:
                    database_json.write(json.dumps(userdb, ensure_ascii=False, indent=4))
                return
            elif e == '<a:no:698461934613168199>':
                await asyncio.gather(msg.delete(),ctx.send(embed=get_embed('<a:no:698461934613168199> | 취소 되었습니다!',"", 0xFF0000)))
                return
    
    @commands.command(name='송금', aliases=['입금'])
    async def _give_money(self, ctx, muser:discord.Member, n:int):
        if ctx.guild is None:
            await ctx.send(embed=get_embed("<a:no:698461934613168199> | 서버내에서만 사용가능한 명령어 입니다.",0xff0000))
            return
        if str(ctx.author.id) not in userdb.keys():
            await ctx.send(embed=get_embed('<a:no:698461934613168199> | 가입 되어 있지 않습니다!',"<알티야 가입> 으로 가입해주세요", 0xFF0000))
            return
        if n <= 0:
            await ctx.send(embed=get_embed("<a:no:698461934613168199> | 1이상의 정수를 입력해주세요!","",0xff0000))
            return
        if str(muser.id) not in userdb.keys():
            await ctx.send(embed=get_embed("<a:no:698461934613168199> | 가입되지 않은 유저입니다","",0xff0000))
            return
        if userdb[str(ctx.author.id)]["money"] < n:
            await ctx.send(embed=get_embed("<a:no:698461934613168199> | 돈이 부족합니다","",0xff0000))
            return
        sendmoney = round( n ** (3/4) )
        msg = await ctx.send(embed=get_embed("📝 | **송금**",f"**{ctx.author}**님이 **{muser}**님에게 송금\n**전송되는 금액 (수수료 차감)** = {sendmoney}"))
        emjs=['<a:yes:698461934198063104>','<a:no:698461934613168199>']
        for em in emjs: await msg.add_reaction(em)
        def check(reaction, user): return user == ctx.author and msg.id == reaction.message.id and str(reaction.emoji) in emjs
        try: reaction, user = await self.client.wait_for('reaction_add', check=check, timeout=20)
        except asyncio.TimeoutError: await asyncio.gather(msg.delete(),ctx.send(embed=get_embed('⏰ | 시간이 초과되었습니다!',"", 0xFF0000)))
        else:
            e = str(reaction.emoji)
            if e == '<a:yes:698461934198063104>':
                userdb[str(ctx.author.id)]["money"] = userdb[str(ctx.author.id)]["money"] - n
                userdb[str(muser.id)]["money"] = userdb[str(muser.id)]["money"] + sendmoney
                await ctx.send(embed=get_embed(f"{ctx.author.name}님이 {muser.name}님에게 송금하셨습니다",f"송금 금액 : {n}\n\n받은 금액 (수수료 차감) : {sendmoney}"))
                with open("./data/userdatabase.json", "w", encoding='utf-8') as database_json: database_json.write(json.dumps(userdb, ensure_ascii=False, indent=4))
                return
            elif e == '<a:no:698461934613168199>':
                await asyncio.gather(msg.delete(),ctx.send(embed=get_embed('<a:no:698461934613168199> | 취소 되었습니다!',"", 0xFF0000)))
                return
        

    @commands.group(name='돈순위', aliases=['순위','랭크','순'], invoke_without_command=True)
    async def _money_rank(self, ctx):
        if str(ctx.author.id) not in userdb.keys():
            await ctx.send(embed=get_embed('<a:no:698461934613168199> | 가입 되어 있지 않습니다!',"<알티야 가입> 으로 가입해주세요", 0xFF0000))
            return
        await ctx.send(embed=get_embed("<a:no:698461934613168199> | 알맞지 않은 명령어입니다","<알티야 돈순위 전체> 또는 <알티야 돈순위 서버> 중 하나를 사용해주세요",0xff0000))
        
    @_money_rank.command(name='서버', aliases=['섭'])
    async def _money_rank_server(self, ctx):
        if str(ctx.author.id) not in userdb.keys():
            await ctx.send(embed=get_embed('<a:no:698461934613168199> | 가입 되어 있지 않습니다!',"<알티야 가입> 으로 가입해주세요", 0xFF0000))
            return
        if ctx.guild is None:
            await ctx.send(embed=get_embed("<a:no:698461934613168199> | 서버내에서만 사용가능한 명령어 입니다.",0xff0000))
            return
        embed=get_embed("알티봇 서버내 돈순위 TOP 10")
        imdic = []
        for a in userdb.keys():
            try: 
                user=ctx.guild.get_member(int(a)).name
                imdic.append([user,userdb[a]["money"]+userdb[a]["bank"]])
            except: pass
        lis = sorted(imdic, key=lambda x:x[1],reverse=True)
        page = 1
        lastpage = round(len(lis)/10)+1
        if len(lis) > 10: r=10
        else: r=len(lis)
        for a in range(0,r):
            if a == 0: medal = "<:1thropy:716106586333904986>"
            elif a == 1: medal = "<:silverthropy:736215959823712306>"
            elif a == 2: medal = "<:bronzethropy:736215949614645269>"
            else: medal = ":medal:"
            embed.add_field(name=f"{medal} {a+1}위 {lis[a][0]}님",value=f"{lis[a][1]}원",inline=False)
        msg=await ctx.send(embed=embed)
        while True:
            if len(lis) <= 9: return
            emjs=['◀️','▶️']
            for em in emjs: await msg.add_reaction(em)
            def check(reaction, user):
                return user == ctx.author and msg.id == reaction.message.id and str(reaction.emoji) in emjs
            try:
                reaction, user = await self.client.wait_for('reaction_add', check=check, timeout=60)
            except asyncio.TimeoutError:
                try: msg.clear_reactions()
                except: pass
            else:
                e = str(reaction.emoji)
                if e == '◀️':
                    if page<=1: continue
                    page-=1
                    embed=get_embed("알티봇 서버내 돈순위 TOP 10")
                    for a in range((page-1)*10,(page-1)*10+10):
                        if a > len(lis)-1: break
                        if a == 0: medal = "<:1thropy:716106586333904986>"
                        elif a == 1: medal = "<:silverthropy:736215959823712306>"
                        elif a == 2: medal = "<:bronzethropy:736215949614645269>"
                        else: medal = ":medal:"
                        embed.add_field(name=f"{medal} {a+1}위 {lis[a][0]}님",value=f"{lis[a][1]}원",inline=False)
                    await msg.edit(content="",embed=embed)
                elif e == '▶️':
                    if page>=lastpage: continue
                    else:
                        page+=1
                        embed=get_embed("알티봇 서버내 돈순위 TOP 10")
                        for a in range((page-1)*10,(page-1)*10+10):
                            if a > len(lis)-1: break
                            embed.add_field(name=f":medal: {a+1}위 {lis[a][0]}님",value=f"{lis[a][1]}원",inline=False)
                        await msg.edit(content="",embed=embed)

        
    @_money_rank.command(name="전체", aliases=['다','전부','전'])
    async def _money_rank_all(self, ctx):
        if str(ctx.author.id) not in userdb.keys(): 
            await ctx.send(embed=get_embed('<a:no:698461934613168199> | 가입 되어 있지 않습니다!',"<알티야 가입> 으로 가입해주세요", 0xFF0000))
            return
        embed=get_embed("알티봇 돈순위 전체 TOP 10")
        imdic = []
        for a in userdb.keys():
            imdic.append([a,userdb[a]["money"]+userdb[a]["bank"]])
        lis = sorted(imdic, key=lambda x:x[1],reverse=True)
        if len(lis) > 10: r=10
        else: r=len(lis)
        page = 1
        lastpage = round(len(lis)/10)+1
        for a in range(0,r):
            try: username=self.client.get_user(int(lis[a][0])).name
            except: username=lis[a][0]
            money=lis[a][1]
            embed.add_field(name=f":medal: {a+1}위 {username}님",value=f"{lis[a][1]}원",inline=False)
        msg=await ctx.send(embed=embed)
        while True:
            if len(lis) <= 9: return
            emjs=['◀️','▶️']
            for em in emjs: await msg.add_reaction(em)
            def check(reaction, user):
                return user == ctx.author and msg.id == reaction.message.id and str(reaction.emoji) in emjs
            try:
                reaction, user = await self.client.wait_for('reaction_add', check=check, timeout=60)
            except asyncio.TimeoutError:
                try: msg.clear_reactions()
                except: pass
            else:
                e = str(reaction.emoji)
                if e == '◀️':
                    if page<=1: continue
                    page-=1
                    embed=get_embed("알티봇 돈순위 전체 TOP 10")
                    for a in range((page-1)*10,(page-1)*10+10):
                        if a > len(lis)-1: break
                        if a == 0: medal = "<:1thropy:716106586333904986>"
                        elif a == 1: medal = "<:silverthropy:736215959823712306>"
                        elif a == 2: medal = "<:bronzethropy:736215949614645269>"
                        else: medal = ":medal:"
                        try: username=self.client.get_user(int(lis[a][0])).name
                        except: username=lis[a][0]
                        embed.add_field(name=f"{medal} {a+1}위 {username}님",value=f"{lis[a][1]}원",inline=False)
                    await msg.edit(content="",embed=embed)
                elif e == '▶️':
                    if page>=lastpage: continue
                    else:
                        page+=1
                        embed=get_embed("알티봇 돈순위 전체 TOP 10")
                        for a in range((page-1)*10,(page-1)*10+10):
                            if a > len(lis)-1: break
                            try: username=self.client.get_user(int(lis[a][0])).name
                            except: username=lis[a][0]
                            embed.add_field(name=f":medal: {a+1}위 {username}님",value=f"{lis[a][1]}원",inline=False)
                        await msg.edit(content="",embed=embed)

    @commands.command(name='돈설정')
    async def _money_set(self,ctx,uid,n:int):
        if str(ctx.author.id) not in userdb.keys(): 
            await ctx.send(embed=get_embed('<a:no:698461934613168199> | 가입 되어 있지 않습니다!',"<알티야 가입> 으로 가입해주세요", 0xFF0000))
            return
        if ctx.author.id not in [467666650183761920, 386715407697969173]: return
        userdb[uid]["money"] = n
        await ctx.send(f"SETTED {uid}\nn: {n}")
        with open("./data/userdatabase.json", "w", encoding='utf-8') as database_json: database_json.write(json.dumps(userdb, ensure_ascii=False, indent=4))

    @commands.command(name='은행설정')
    async def _bank_set(self, ctx, uid, n:int):
        if str(ctx.author.id) not in userdb.keys(): 
            await ctx.send(embed=get_embed('<a:no:698461934613168199> | 가입 되어 있지 않습니다!',"<알티야 가입> 으로 가입해주세요", 0xFF0000))
            return
        if ctx.author.id not in [467666650183761920, 386715407697969173]: return
        userdb[uid]["bank"] = n
        await ctx.send(f"SETTED BANK {uid}\nn: {n}")
        with open("./data/userdatabase.json", "w", encoding='utf-8') as database_json: database_json.write(json.dumps(userdb, ensure_ascii=False, indent=4))

    # 알파 왔다감
    @commands.command(name='강제가입')
    async def _force_register(self, ctx: commands.Context, uid):
        if ctx.author.id not in [467666650183761920, 386715407697969173]: return

        if uid in userdb.keys(): 
            await ctx.send('이미 가입된 유저: {}'.format(uid))
        else:
            userdb[uid] = {"money":5000,"bank":0}
            with open("./data/userdatabase.json", "w", encoding='utf-8') as database_json:
                database_json.write(json.dumps(userdb, ensure_ascii=False, indent=4))
            await ctx.send('완료: {}'.format(uid))

    # 알파 왔다감
    @commands.command(name='유저등록확인')
    async def _check_user_existing(self, ctx: commands.Context, uid):
        if ctx.author.id not in [467666650183761920, 386715407697969173]: return

        if uid in userdb.keys(): 
            await ctx.send('가입된 유저: {}\n돈: {} 원\n은행: {} 원'.format(uid, userdb[uid]['money'], userdb[uid]['bank']))
        else:
            await ctx.send('가입 안된 유저: {}'.format(uid))

    @commands.group(name='저금', invoke_without_command=True)
    async def _money_save(self, ctx, n:int):
        if str(ctx.author.id) not in userdb.keys(): 
            await ctx.send(embed=get_embed('<a:no:698461934613168199> | 가입 되어 있지 않습니다!',"<알티야 가입> 으로 가입해주세요", 0xFF0000))
            return
        if userdb[str(ctx.author.id)]["money"] < n:
            await ctx.send(embed=get_embed("<a:no:698461934613168199> | 금액이 너무 큽니다","",0xff0000))
            return
        if n < 0: raise errors.morethan1
        userdb[str(ctx.author.id)]["bank"] = userdb[str(ctx.author.id)]["bank"] + n
        userdb[str(ctx.author.id)]["money"] = userdb[str(ctx.author.id)]["money"] - n
        await ctx.send(embed=get_embed("<a:yes:698461934198063104> | 저금 완료!"))
        with open("./data/userdatabase.json", "w", encoding='utf-8') as database_json: database_json.write(json.dumps(userdb, ensure_ascii=False, indent=4))

    @_money_save.command(name='전체', aliases=['다','올인'])
    async def _money_save_all(self, ctx):
        if str(ctx.author.id) not in userdb.keys(): 
            await ctx.send(embed=get_embed('<a:no:698461934613168199> | 가입 되어 있지 않습니다!',"<알티야 가입> 으로 가입해주세요", 0xFF0000))
            return
        userdb[str(ctx.author.id)]["bank"] = userdb[str(ctx.author.id)]["bank"] + userdb[str(ctx.author.id)]["money"]
        userdb[str(ctx.author.id)]["money"] = 0 
        await ctx.send(embed=get_embed("<a:yes:698461934198063104> | 저금 완료!"))
        with open("./data/userdatabase.json", "w", encoding='utf-8') as database_json: database_json.write(json.dumps(userdb, ensure_ascii=False, indent=4))

    @commands.group(name='인출', invoke_without_command=True)
    async def _money_withdraw(self, ctx, n:int):
        if str(ctx.author.id) not in userdb.keys(): 
            await ctx.send(embed=get_embed('<a:no:698461934613168199> | 가입 되어 있지 않습니다!',"<알티야 가입> 으로 가입해주세요", 0xFF0000))
            return
        if userdb[str(ctx.author.id)]["bank"] < n:
            await ctx.send(embed=get_embed("<a:no:698461934613168199> | 금액이 너무 큽니다","",0xff0000))
            return
        if n < 0: raise errors.morethan1
        userdb[str(ctx.author.id)]["bank"] = userdb[str(ctx.author.id)]["bank"] - n
        userdb[str(ctx.author.id)]["money"] = userdb[str(ctx.author.id)]["money"] + n
        await ctx.send(embed=get_embed("<a:yes:698461934198063104> | 인출 완료!"))
        with open("./data/userdatabase.json", "w", encoding='utf-8') as database_json: database_json.write(json.dumps(userdb, ensure_ascii=False, indent=4))

    @_money_withdraw.command(name='전체', aliases=['다','올인'])
    async def _money_withdraw_all(self, ctx):
        if str(ctx.author.id) not in userdb.keys():
            await ctx.send(embed=get_embed('<a:no:698461934613168199> | 가입 되어 있지 않습니다!',"<알티야 가입> 으로 가입해주세요", 0xFF0000))
            return
        userdb[str(ctx.author.id)]["money"] = userdb[str(ctx.author.id)]["money"] + userdb[str(ctx.author.id)]["bank"]
        userdb[str(ctx.author.id)]["bank"] = 0
        await ctx.send(embed=get_embed("<a:yes:698461934198063104> | 인출 완료!"))
        with open("./data/userdatabase.json", "w", encoding='utf-8') as database_json: database_json.write(json.dumps(userdb, ensure_ascii=False, indent=4))

    @commands.command(name='은행잔고', aliases=['잔고','은행'])
    async def bank_money(self, ctx):
        if str(ctx.author.id) not in userdb.keys():
            await ctx.send(embed=get_embed('<a:no:698461934613168199> | 가입 되어 있지 않습니다!',"<알티야 가입> 으로 가입해주세요", 0xFF0000))
            return
        await ctx.send(embed=get_embed(f"💳 | {ctx.author} 님의 은행잔고","{} 원".format(userdb[str(ctx.author.id)]["bank"])))

def setup(client):
    client.add_cog(money(client))

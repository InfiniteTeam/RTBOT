import discord, requests, datetime, bs4, urllib, asyncio
from discord.ext import commands
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request

def get_embed(title, description='', color=0xCCFFFF): 
    return discord.Embed(title=title,description=description,color=color)

class crawling(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name='실검')
    async def chat_naver(self, ctx):
        msg = await ctx.send("<a:698813836106661889:712170404869046334> 불러오는 중입니다...")
        lis=[]
        for r in requests.get('https://www.naver.com/srchrank?frm=main').json().get("data")[:10]:
            lis.append(f"**{r.get('rank')}위** : [{r.get('keyword')}](https://search.naver.com/search.naver?where=nexearch&query={r.get('keyword').replace(' ', '+')})")
        embed=discord.Embed(title=f"<:Naver_Icon_2014:713189615271542886> | 네이버 실검정보", description="\n".join(lis),colour=0xccffff, timestamp=datetime.datetime.utcnow())
        await asyncio.gather(msg.delete(),ctx.send(embed=embed))

    @commands.command(name='노래순위')
    async def chat_kpop(self, ctx):
        msg = await ctx.send("<a:698813836106661889:712170404869046334> 불러오는 중입니다...")
        soup = BeautifulSoup(requests.get('https://search.naver.com/search.naver?sm=top_hty&fbm=0&ie=utf8&query=%EB%84%A4%EC%9D%B4%EB%B2%84+%EB%AE%A4%EC%A7%81').text, 'html.parser')
        embed = discord.Embed(title='🎵 | **멜론차트 TOP 10**',color=0xCCFFFF)
        for a in range(1,11):
            embed.add_field(name=f'Top{a} '+soup.select('#main_pack > div.sc.sp_music._prs_mus_sen > div.api_subject_bx.type_slim.music_chart > ol > li:nth-child('+str(a)+') > div > div.music_area > div.music_info > div.title > a')[0].text,value=soup.select('#main_pack > div.sc.sp_music._prs_mus_sen > div.api_subject_bx.type_slim.music_chart > ol > li:nth-child('+str(a)+') > div > div.music_area > div.music_info > div.info > a.singer')[0].text,inline=False)
        await asyncio.gather(msg.delete(),ctx.send(embed=embed))

    @commands.command(name='코로나')
    async def chat_corona(self, ctx):
        msg = await ctx.send("<a:698813836106661889:712170404869046334> 불러오는 중입니다...")
        soup = BeautifulSoup(requests.get('https://search.naver.com/search.naver?sm=top_hty&fbm=0&ie=utf8&query=%EC%BD%94%EB%A1%9C%EB%82%98+%ED%99%95%EC%A7%84%EC%9E%90').text, 'html.parser')
        a1 = soup.select('#main_pack > div.content_search.section > div > div > div > div.production_main > div > div.main_detail_bx > div:nth-child(2) > div.state_area > div > div > div:nth-child(1) > div > p > strong')
        a2 = soup.select('#main_pack > div.content_search.section > div > div > div > div.production_main > div > div.main_detail_bx > div:nth-child(2) > div.state_area > div > div > div:nth-child(2) > div > p > strong')
        a3 = soup.select('#main_pack > div.content_search.section > div > div > div > div.production_main > div > div.main_detail_bx > div:nth-child(2) > div.state_area > div > div > div:nth-child(3) > div > p > strong')
        a4 = soup.select('#main_pack > div.content_search.section > div > div > div > div.production_main > div > div.main_detail_bx > div:nth-child(2) > div.state_area > div > div > div:nth-child(4) > div > p > strong')
        embed=discord.Embed(title='💊 | **코로나19 국내 현황**', description=f'**국내 기준**\n확진자 : {a1[0].text} 명\n격리 해제 : {a2[0].text} 명\n검사 진행 : {a3[0].text} 명\n사망자 : {a4[0].text} 명', color=0xCCFFFF, timestamp=datetime.datetime.utcnow())
        await asyncio.gather(msg.delete(),ctx.send(embed=embed))

    @commands.command(name='빌보드')
    async def chat_billboard(self, ctx):
        msg = await ctx.send("<a:698813836106661889:712170404869046334> 불러오는 중입니다...")
        soup = BeautifulSoup(requests.get('https://www.billboard.com/charts/hot-100').text, 'html.parser')
        embed = discord.Embed(title='🎵 | **BillBoard TOP 10**',color=0xCCFFFF)
        for a in range(1,11):
            embed.add_field(name='Top'+str(a)+' '+soup.select('#charts > div > div.chart-list.container > ol > li:nth-child('+str(a)+') > button > span.chart-element__information > span.chart-element__information__song.text--truncate.color--primary')[0].text,value=soup.select('#charts > div > div.chart-list.container > ol > li:nth-child('+str(a)+') > button > span.chart-element__information > span.chart-element__information__artist.text--truncate.color--secondary')[0].text,inline=False)
        await asyncio.gather(msg.delete(),ctx.send(embed=embed))

    @commands.command(name='데몬')
    async def chat_demon(self, ctx):
        msg = await ctx.send("<a:698813836106661889:712170404869046334> 불러오는 중입니다...")
        req = requests.get('https://www.pointercrate.com/demonlist/') 
        soup = BeautifulSoup(req.text, 'html.parser')
        embed=discord.Embed(title='지메 실시간 데몬 리스트', color=0xCCFFFF, timestamp=datetime.datetime.utcnow())
        for a in range(3,13):
            level=soup.select('body > div > main > section:nth-child('+str(a)+') > div > div.leftlined.pad > h2 > a')
            if a == 3: medal = ':first_place:'
            elif a == 4: medal = ':second_place:'
            elif a == 5: medal = ':third_place:'
            else : medal = ":medal:"
            embed.add_field(name=medal+str(int(a)-2)+'위',value=level[0].text,inline=False)
        await asyncio.gather(msg.delete(),ctx.send(embed=embed))

def setup(client):
    client.add_cog(crawling(client))
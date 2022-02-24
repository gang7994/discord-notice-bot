import discord
import requests
from bs4 import BeautifulSoup
import asyncio
import os

client = discord.Client() #디스코드와 봇과의 연결을 client변수에 할당


univ_url = "http://computing.hanyang.ac.kr/open/notice.php"
sw_url = "http://computing.hanyang.ac.kr/open/deptNotice.php"
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36"}

@client.event
async def on_ready():
    print("봇이 온라인으로 전환되었습니다.")

@client.event
async def on_message(message):
    if message.content == "!info":
        embed = discord.Embed(title="명령어")

        embed.set_author(name="SW Notice Bot", url="https://github.com/gang7994/discord-notice-bot.git", icon_url="https://www.hanyang.ac.kr/documents/20182/73809/HYU_symbol_basic_png.png/72485650-ecb2-4007-a0ed-bc4b5c0d323b?t=1474070402203")
        embed.add_field(name="!info", value="정보\n", inline=False)
        embed.add_field(name="!clear", value="메세지 10개 삭제\n", inline=False)
        embed.add_field(name="!대학공지", value="대학 공통공지 출력\n", inline=False)
        embed.add_field(name="!학과공지", value="학과 공지 출력\n", inline=False)
        embed.add_field(name="URL", value="[ERICA소프트웨어융합대학](http://computing.hanyang.ac.kr/)", inline=True)

        await message.channel.send(embed=embed)
        
    
    if message.content.startswith("!clear"):
        purge_number = '100'
        check_purge_number = purge_number.isdigit()

        if check_purge_number == True:
            await message.channel.purge(limit=int(purge_number) + 1)
            msg = await message.channel.send(f"**{purge_number}개**의 메시지를 삭제했습니다.")
            await asyncio.sleep(5)
            await msg.delete()

        else:
            await message.channel.send("올바른 값을 입력해주세요.")
    
        
    if message.content.startswith("!대학공지"):  
        url = univ_url
        res = requests.get(url, headers=headers).text
        soup = BeautifulSoup(res, "lxml")
        notices = soup.find("table", attrs={"class":"bbs_con"}).find("tbody").find_all("tr")
        embed = discord.Embed(title="[대학공지]")
        embed.set_author(name="SW Notice Bot", url="https://github.com/gang7994/discord-notice-bot.git", icon_url="https://hywiki.s3.amazonaws.com/thumb/f/fe/%EC%86%8C%ED%94%84%ED%8A%B8%EC%9B%A8%EC%96%B4%ED%95%99%EB%B6%80.jpg/300px-%EC%86%8C%ED%94%84%ED%8A%B8%EC%9B%A8%EC%96%B4%ED%95%99%EB%B6%80.jpg")        
        a,b=0,0
        for notice in notices:
            col = notice.find_all("td")
            num = col[0]
            name = col[1].get_text()
            day = col[2].get_text()
            link = col[1].a["href"]
            url_link = "http://computing.hanyang.ac.kr" + link
            if num.get_text() == "[공지]":
                if a==0:
                    embed.add_field(name="[공지]", value='[%s](%s)%s' % (name,url_link,day), inline=False)
                a+=1
                if a > 7:
                    continue
                elif a != 1:
                    embed.add_field(name="▽", value='[%s](%s)%s' % (name,url_link,day), inline=False)
            else:
                if b==0:
                    embed.add_field(name="[일반]", value='[%s](%s)%s' % (name,url_link,day), inline=False)
                b+=1
                if b > 9:
                    continue
                elif b!=1:
                    embed.add_field(name="▽", value='[%s](%s)%s' % (name,url_link,day), inline=False)         
        await message.channel.send(embed=embed)
    
    if message.content.startswith("!학과공지"):  
        url = sw_url
        res = requests.get(url, headers=headers).text
        soup = BeautifulSoup(res, "lxml")
        notices = soup.find("table", attrs={"class":"bbs_con"}).find("tbody").find_all("tr")
        embed = discord.Embed(title="[학과공지]")
        embed.set_author(name="SW Notice Bot", url="https://github.com/gang7994/discord-notice-bot.git", icon_url="https://hywiki.s3.amazonaws.com/thumb/f/fe/%EC%86%8C%ED%94%84%ED%8A%B8%EC%9B%A8%EC%96%B4%ED%95%99%EB%B6%80.jpg/300px-%EC%86%8C%ED%94%84%ED%8A%B8%EC%9B%A8%EC%96%B4%ED%95%99%EB%B6%80.jpg")
        a,b=0,0
        for notice in notices:
            col = notice.find_all("td")
            num = col[0]
            name = col[1].get_text()
            day = col[2].get_text()
            link = col[1].a["href"]
            url_link = "http://computing.hanyang.ac.kr" + link
            if "[인공지능학과]" in name:
                continue
            else:
                if num.get_text() == "[공지]":
                    if a==0:
                        embed.add_field(name="[공지]", value='[%s](%s)%s' % (name,url_link,day), inline=False)
                    a+=1
                    if a > 7:
                        continue
                    elif a != 1:
                        embed.add_field(name="▽", value='[%s](%s)%s' % (name,url_link,day), inline=False)
                else:
                    if b==0:
                        embed.add_field(name="[일반]", value='[%s](%s)%s' % (name,url_link,day), inline=False)
                    b+=1
                    if b > 9:
                        continue
                    elif b!=1:
                        embed.add_field(name="▽", value='[%s](%s)%s' % (name,url_link,day), inline=False)     
        await message.channel.send(embed=embed)
access_token = os.environ['BOT_TOKEN']
client.run(access_token) 

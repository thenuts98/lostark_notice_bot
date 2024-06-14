import notice
import discord
from dotenv import load_dotenv
import os
import aiohttp
import asyncio
import datetime, time
import requests

load_dotenv()

hook_url = os.environ.get('WEBHOOK_URL') # 웹훅 dir은 credential하기에 .env로 관리
f_code = os.environ.get('CODE_DIR') # 사용할 시스템마다 다르기 따문에 .env에 저장
flaks_url = 'http://127.0.0.1:5000/status'
image_url = 'https://cdn-lostark.game.onstove.com/2018/obt/assets/images/common/thumb/logo.png' # 로스트아크 아이콘

def make_embed(code):
    """
    `code`에서 `embed` 생성\n
    `get_notice`에서 return 받은 데이터를 사용해 각 attribute 형성
    """
    notice_url = notice.url + '/Views/' + str(code)
    notice_kind, notice_title, notice_content = notice.get_notice(code)
    emb = discord.Embed(title=notice_kind + ' | ' + notice_title, 
                        url = notice_url,
                        description=notice_content
                        )
    emb.set_thumbnail(url=image_url)
    return emb

async def send_webhook(emb):
    async with aiohttp.ClientSession() as session:
        webhook = discord.Webhook.from_url(hook_url, session=session)
        await webhook.send(embed=emb)


if __name__ == '__main__':
    
    notice_list = notice.get_notice_code() # 현재 목록 추출
    notice_list.sort() # 오름차순 정리
    #print(notice_list)
    with open(f_code, 'r') as f:
        recent_code = f.readline() # 마지막으로 전송한 공지 코드
    #print('최근 전송한 notice code :', recent_code)
    try:
        for i in notice_list:
            if int(i) > int(recent_code):
                with open(f_code, 'w') as f:    
                    f.write(i)
                emb = make_embed(i)
                asyncio.run(send_webhook(emb))
                print(f'{i}번 공지 전송')
        post_data = {
            'time' : datetime.datetime.now(),
            'status' : 'online'
        }
        requests.post(flaks_url, data=post_data)
    except Exception as e:
        print(e)   


    # for i in notice_list:
    #     try:
    #         emb = make_embed(i)
    #         asyncio.run(send_webhook(emb))
    #     except Exception as e:
    #         print(e)
                
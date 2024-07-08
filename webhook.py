import notice
import discord
from dotenv import load_dotenv
import os
import aiohttp
import asyncio
import datetime, time
import requests
import pandas as pd

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


def make_embed_api(series):
    """
    DataFrame의 조건에 해당하는 한 series에 대해 embed 형성
    """
    notice_url = series['Link']
    notice_kind = series['Type']
    notice_title = series['Title']
    emb = discord.Embed(title=notice_kind + ' | ' + notice_title, 
                        url = notice_url,
                        )
    emb.set_thumbnail(url=image_url)
    return emb

async def send_webhook(emb):
    async with aiohttp.ClientSession() as session:
        webhook = discord.Webhook.from_url(hook_url, session=session)
        await webhook.send(embed=emb)


def webhook():
    print(f'{str(datetime.datetime.now())} 동작')
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
                print(f'{str(datetime.datetime.now())} : {i}번 공지 전송')
        
        # 웹사이트에 동작 상태 전송
        # post_data = {
        #     'time' : datetime.datetime.now(),
        #     'status' : 'online'
        # }
        # requests.post(flaks_url, data=post_data)

    except Exception as e:
        print(str(datetime.datetime.now()), end='\t' ) 
        print(e)  

def webhook_api():
    print(f'{str(datetime.datetime.now())} 동작')
    df_notice = notice.get_notice_api()
    with open(f_code, 'r') as f:
        recent_code = f.readline() # 마지막으로 전송한 공지 코드
    df_notice = df_notice[df_notice['code'] > int(recent_code)]
    df_notice = df_notice.reset_index(drop=True)

    for i in range(len(df_notice)):
        with open(f_code, 'w') as f:    
            f.write(str(df_notice.loc[i]['code']))
        emb = make_embed(df_notice.loc[i])
        asyncio.run(send_webhook(emb))
        print(f'{str(datetime.datetime.now())} : {df_notice.loc[i]["code"]}번 공지 전송')

if __name__ == '__main__':
    try:
        webhook_api()
    except Exception as e:
        print(f'{str(datetime.datetime.now())} : {e}')


    # for i in notice_list:
    #     try:
    #         emb = make_embed(i)
    #         asyncio.run(send_webhook(emb))
    #     except Exception as e:
    #         print(e)
                
import notice
import discord
from dotenv import load_dotenv
import os
import aiohttp
import asyncio

load_dotenv()

hook_url = os.environ.get('WEBHOOK_URL')
image_url = 'https://cdn-lostark.game.onstove.com/2018/obt/assets/images/common/thumb/logo.png'

def make_embed(code):
    """
    `code`에서 `embed` 생성
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
    
    notice_list = notice.get_notice_code()
    notice_list.sort()
    print(notice_list)
    with open('code', 'r') as f:
        recent_code = f.readline()
    print('최근 전송한 notice code :', recent_code)
    try:
        for i in notice_list:
            
            if int(i) > int(recent_code):
                with open('code', 'w') as f:    
                    f.write(i)
                emb = make_embed(i)
                asyncio.run(send_webhook(emb))
                print(f'{i}번 공지 전송')
                
    except Exception as e:
        print(e.text)   


    # for i in notice_list:
    #     try:
    #         emb = make_embed(i)
    #         asyncio.run(send_webhook(emb))
    #     except Exception as e:
    #         print(e)
            
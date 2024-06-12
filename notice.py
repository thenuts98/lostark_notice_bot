import requests
from bs4 import BeautifulSoup
import time, datetime


url = "https://lostark.game.onstove.com/News/Notice" # 로스트아크 공지페이지 주소



def get_notice_code(url = url + '/List'):
    """url에서 공지 목록 추출, 코드 list로 반환\n
    url에서 5자리 공지 코드를 추출합니다.\n
    6자리 되기 전에 섭종할듯\n

    """
    with requests.get(url) as r:

        notice_list = [] 
        soup = BeautifulSoup(r.text, "html.parser")

        # 웹페이지별 하드 코딩
        notice = soup.find_all('ul')[11] 
        notice = notice.find_all('a')
        # print(notice_list)

        for idx, i in enumerate(notice):
            # print(idx, i['href'][19:24])
            notice_list.append(i['href'][19:24])


    return notice_list

    
def get_notice(code):
    """ 주어진 코드 공지의 제목, 내용, 이미지 등 embed에 사용할 정보 구성
    embed reference : https://discordpy.readthedocs.io/en/stable/api.html#embed
    """
    global url
    notice_url = url + '/Views/' + str(code)
    with requests.get(notice_url) as r:
        soup = BeautifulSoup(r.text, "html.parser")

        
        notice_kind = (soup.select('span.category.category--notice')[0].text) # 공지 종류
        notice_title = (soup.select('span.article__title')[0].text) # 공지 제목
        notice_content = (soup.select('div.fr-view')[0].text) # 공지 내용  
        notice_content = notice_content.split('.')
        notice_content = '\n\n'.join(notice_content[:4])

        return notice_kind, notice_title, notice_content
        
        
    
if __name__ == '__main__':
    notice_list = get_notice_code()
    get_notice(notice_list[0])
    



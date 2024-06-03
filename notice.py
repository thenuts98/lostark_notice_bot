import requests
from bs4 import BeautifulSoup


url = "https://lostark.game.onstove.com/News/Notice/List" # 로스트아크 공지페이지 주소


def get_notice(url = url):
    """url에서 공지 목록 추출, list로 반환
    """
    with requests.get(url) as r:
        
        soup = BeautifulSoup(r.text, "html.parser")
        notice_list = soup.find_all('ul')[11]
        
        notice_list = notice_list.find_all('a')
        # print(notice_list)

        for idx, i in enumerate(notice_list):
            print(idx, i['href'][19:24])



    return notice_list

    

if __name__ == '__main__':
    get_notice()

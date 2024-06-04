import requests
from bs4 import BeautifulSoup


url = "https://lostark.game.onstove.com/News/Notice" # 로스트아크 공지페이지 주소


def get_notice_code(url = url + '/List'):
    """url에서 공지 목록 추출, 코드 list로 반환
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
    """
    global url
    notice_url = url + '/Views/' + str(code)
    with requests.get(notice_url) as r:
        print(r)
if __name__ == '__main__':

    notice_list = get_notice_code()

    for i in notice_list:
        get_notice(i.text)


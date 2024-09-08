from dotenv import load_dotenv
import os, sys
import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import webhook

load_dotenv()

api_url = "https://developer-lostark.game.onstove.com/auctions/items"
api_key = os.getenv('API_KEY')

# 현재 경로 추가


json_template_path = "/home/kimnuts/working/lostark_auction/request.json"

# 아크패시브 옵션 딕셔너리
ark_option_dict = {
    "공격력 %" : 45,
    "무기 공격력 %" : 46,
    "적에게 주는 피해 증가" : 42,
    "추가 피해" : 41,
    "치명타 적중률" : 49,
    "치명타 피해" : 50
}

ark_value_dict = {
    "상" : 3,
    "중" : 2,
    "하" : 1
}

def ark_data_parser(option):
    """
    아크패시브 옵션 데이터를 파싱하여 get_auction_data 함수에 넘김
    예) 목걸이 상상으로 주어지면 get_auction_data(json_data, "적에게 주는 피해 증가", "상", "추가 피해", "상") 으로 전달
    """
    option = option.split(" ")
    if option[0] == "목걸이":
        options = ["추가 피해", "적에게 주는 피해 증가"]
    elif option[0] == "반지":
        options = ["치명타 적중률", "치명타 피해"]
    elif option[0] == "귀걸이":
        options = ["무기 공격력 %", "공격력 %"]

    if len(option[1]) == 2:
        price = min(get_auction_data( first_option=options[0], first_value=option[1][0], second_option=options[1], second_value=option[1][1] ),
                    get_auction_data( first_option=options[1], first_value=option[1][0], second_option=options[0], second_value=option[1][1]))
    else:
        price = min(get_auction_data( first_option=options[0], first_value=option[1]),
                    get_auction_data( first_option=options[1], first_value=option[1]))
                    
    return price




def get_auction_data( first_option = "공격력 %", first_value = "상", second_option = None, second_value = None):
    """
    주어진 옵션에 대해 검색하여 최저가 반환
    """
    try:
        with open(json_template_path, 'r', encoding='UTF-8') as f:
            json_data = json.load(f)

        headers = {
            'Authorization': api_key,
            'accept': 'application/json'
        }
        json_data['EtcOptions'][0]['SecondOption'] = ark_option_dict[first_option] 
        json_data['EtcOptions'][0]['MinValue'] = ark_value_dict[first_value]

        if second_option != None:
            json_data['EtcOptions'].append({
                "FirstOption": 7,
                "SecondOption": ark_option_dict[second_option],
                "MinValue": ark_value_dict[second_value],
                "MaxValue": 3
            })
        
    
        # 즉구가 반환
        json_data['Sort'] = "BUY_PRICE"
        response = requests.post(api_url, headers=headers, json=json_data)
        response_json = response.json()

        buy_price = response_json['Items'][0]['AuctionInfo']['BuyPrice']


        # 입찰가 반환
        json_data['Sort'] = "BIDSTART_PRICE"
        response = requests.post(api_url, headers=headers, json=json_data)
        response_json = response.json()
        
        bid_price = response_json['Items'][0]['AuctionInfo']['BidStartPrice']

        
        if bid_price < buy_price * 0.9 and (first_value == '상' or (first_value == '중' and second_value == '중')):
            webhook.webhook_ark(buy_price, bid_price, first_option, first_value, second_value)
        
        print(buy_price, bid_price)

        return bid_price
    except:
        return 0
    # if response.status_code == 200:
    #     print("Success:", response.json())
    # else:
    #     print("Failed:", response.status_code, response.text)

# 함수 호출


def price_dataframe():
    """
    상상, 상중, 상하, 상, 중중, 중하, 하하, 하 순으로 가격 표시하는 데이터프레임 생성 
    """
    data = {
    '목걸이': [0, 0, 0, 0, 0, 0, 0, 0],
    '귀걸이': [0, 0, 0, 0, 0, 0, 0, 0],
    '반지': [0, 0, 0, 0, 0, 0, 0, 0]
    }

    # 행 이름 지정
    index = ['상상', '상중', '상하', '상', '중중', '중하', '하하', '하']
    item  = [ '목걸이', '귀걸이', '반지']

    for i in item:
        for idx, option in enumerate(index):
            data[i][idx] = ark_data_parser( f"{i} {option}")
            print(f"{i} {option} 검색")

    # DataFrame 생성
    df = pd.DataFrame(data, index=index)


    return df



if __name__ == "__main__":

    # print(get_auction_data(json_data, first_option=ark_option_dict['공격력 %'], first_value=3))
    
    
    df = price_dataframe()
    excel_file_path = 'output.xlsx'
    df.to_excel(excel_file_path)
    print(df)
    
    # get_auction_data(first_option="추가 피해")



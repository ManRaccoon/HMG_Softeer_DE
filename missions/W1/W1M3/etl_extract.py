import requests
from bs4 import BeautifulSoup
import json

# url에서 table을 가져와 json파일로 저장
def extract_GDP(url, path):
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')

    # selector 요소로 테이블 요소 추출
    table = soup.select_one("table.wikitable.sortable > tbody")
    
    # 헤더를 제외한 열 정보 추출
    tr = table.find_all('tr')[3:] 
    
    # JSON형식 데이터 생성
    result = []

    # 열 정보를 통해 행 정보 추출
    for rows in tr:
        td = rows.find_all('td')

        # Country, GDP(Billon), Year요소 추출
        Country = td[0].text.strip()
        GDP = td[1].text.strip()
        Year = td[2].text.strip()

        # GDP가 존재하지 않으면 제외
        if GDP == "\u2014":
            continue

        # Dict 형식으로 변환 후 result에 저장
        result.append({
            "Country" : Country,
            "GDP" : GDP,
            "Year" : Year
        })

    # result를 JSON파일 형식으로 저장
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=4)
import requests
from bs4 import BeautifulSoup
import pandas as pd

GDP_url = 'https://en.wikipedia.org/wiki/List_of_countries_by_GDP_%28nominal%29'

Region_url = {'African' : 'https://en.wikipedia.org/wiki/List_of_African_countries_by_GDP_(nominal)',
            'Arab_League' : 'https://en.wikipedia.org/wiki/List_of_Arab_League_countries_by_GDP_(nominal)',
            'Asia_Pacific' : 'https://en.wikipedia.org/wiki/List_of_countries_in_Asia-Pacific_by_GDP_(nominal)',
            'Commonwealth' : 'https://en.wikipedia.org/wiki/List_of_Commonwealth_of_Nations_countries_by_GDP_(nominal)',
            'Latin_American_Caribbean' : 'https://en.wikipedia.org/wiki/List_of_Latin_American_and_Caribbean_countries_by_GDP_(nominal)',
            'North_American' : 'https://en.wikipedia.org/wiki/List_of_North_American_countries_by_GDP_(nominal)',
            'Oceanian' : 'https://en.wikipedia.org/wiki/List_of_Oceanian_countries_by_GDP',
            'sovereign' : 'https://en.wikipedia.org/wiki/List_of_sovereign_states_in_Europe_by_GDP_(nominal)',}

def extract_GDP(url):
    pass

def extract_Region(url):
    region_df = pd.DataFrame()
    for region, url in region_url.items():
            html = requests.get(url).text
            soup = BeautifulSoup(html, 'html.parser')

            #테이블 요소 가져옴
            table = soup.select_one("table.wikitable.sortable")
            df = pd.read_html(str(table))[0]
            
            # Country라는 이름을 포함한 열만 필터링하여 전부 Country라고 통일
            df = df.filter(like='Country', axis=1)
            df.columns = ['Country']
            df['Country'] = df['Country'].str.extract(r'^([^\[]+)')[0].str.strip()

            # Region명을 적어줌
            df["Region"] = region

            # DataFrame에 저장
            region_df = pd.concat([region_df, df])
    return region_df
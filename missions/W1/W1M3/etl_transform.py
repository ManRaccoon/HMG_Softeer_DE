import pandas as pd
import pycountry_convert as pc

# 저장할 형태로 JSON데이터를 변형
def transform_GDP(path):
    # JSON파일을 DataFrame으로 변환
    df = pd.read_json(path)

    # GDP 단위 변환 (Millon -> Billion)
    df["GDP"] = df["GDP"].replace(',', "", regex=True)
    df["GDP"] = round(df["GDP"].astype(float) / 1000, 2)

    # Year의 주석을 정규식을 통해 제거
    df["Year"] = df["Year"].astype(str)
    df["Year"] = df["Year"].str.extract(r'(\d{4})')[0].astype(int)

    #  Region 열 추가
    df["Region"] = df["Country"].apply(continent_convert)

    return df

# 국가명 -> alpha2 -> 대륙 코드 -> 대륙명으로 바꾸는 함수
def continent_convert(country):
    try:
        alpha2 = pc.country_name_to_country_alpha2(country)
        continent_code = pc.country_alpha2_to_continent_code(alpha2)
        return pc.convert_continent_code_to_continent_name(continent_code)
    except Exception:
        return None
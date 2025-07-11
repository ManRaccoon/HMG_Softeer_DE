import sqlite3
import pandas as pd

# JSON경로 이용하여 GDP가 100B 이상인 나라 출력
def gdp_over_100b(LOAD_JSON_PATH):
    df = pd.read_json(LOAD_JSON_PATH)
    print('- GDP over 100B USD with JSON')
    result = df.loc[df.GDP >= 100]
    result.columns = ["Country", "1B_GDP", "Year", "Continent"]
    print(result)
    

# JSON경로 이용하여 Region별 TOP 5 국가의 GDP 평균 출력
def gdp_region_avg(LOAD_JSON_PATH):
    df = pd.read_json(LOAD_JSON_PATH)
    print('- Averge GDP from Regions\' top 5 with JSON')
    region_top5 = df.sort_values(['Region', 'GDP'], ascending=[True, False]).groupby('Region').head(5)
    result = region_top5.groupby('Region')['GDP'].mean().reset_index()
    result.columns = ["Regions", "Average of TOP 5's GDP"]
    print(result)

# SQL을 이용하여 GDP가 100B 이상인 나라 출력
def gdp_over_100b_db(LOAD_DB_PATH):
    conn = sqlite3.connect(LOAD_DB_PATH)
    cursor = conn.cursor()
    print('- GDP over 100B USD with DB')
    result = cursor.execute( 
    '''
        SELECT *
        FROM Countries_by_GDP
        WHERE GDP > 100
        ORDER BY GDP DESC
    ''')
    result = pd.DataFrame(result.fetchall())
    conn.close()
    result.columns = ["Country", "1B_GDP", "Year", "Continent"]
    print(result)

# SQL을 이용하여 Region별 TOP 5 국가의 GDP 평균 출력
def gdp_region_avg_db(LOAD_DB_PATH):
    conn = sqlite3.connect(LOAD_DB_PATH)
    cursor = conn.cursor()
    print('- Averge GDP from Regions\' top 5 with DB')
    result = cursor.execute( 
    '''
        SELECT Region, AVG(GDP) AS avg_gdp
        FROM (
            SELECT *
            FROM Countries_by_GDP AS a
            WHERE (
                SELECT COUNT(*) 
                FROM Countries_by_GDP AS b
                WHERE a.Region = b.Region AND b.GDP > a.GDP
            ) < 5
        )
        WHERE Region IS NOT Null
        GROUP BY Region;
    ''')
    result = pd.DataFrame(result.fetchall())
    conn.close()
    result.columns = ["Regions", "Average of TOP 5's GDP"]
    print(result)
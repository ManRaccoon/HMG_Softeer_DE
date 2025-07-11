import pandas as pd
import json
import sqlite3

# SQL문을 통해 한 줄씩 비교해가며 중복되지 않는 데이터만 DB 저장
def load_GDP(path, df):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(df.to_dict(orient="records"), f, indent=4)

# SQL문을 통해 한 줄씩 비교해가며 중복되지 않는 데이터만 DB 저장
def load_GDP_db(path, df):
    # SQL 생성
    conn = sqlite3.connect(path)
    cursor = conn.cursor()

    # table 생성
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS "Countries_by_GDP" (
            Country TEXT,
            GDP REAL,
            Year INTEGER,
            Region TEXT,
            PRIMARY KEY (Country, Year)
        )
    ''')

    # DataFrame을 하나씩 비교하며 중복되지 않는 데이터만 삽입
    for _, row in df.iterrows():
        cursor.execute(f'''
            INSERT OR IGNORE INTO "Countries_by_GDP" (Country, GDP, Year, Region)
            VALUES (?, ?, ?, ?)
        ''', (row["Country"], row["GDP"], row["Year"], row["Region"]))
    
    conn.commit()
    conn.close()
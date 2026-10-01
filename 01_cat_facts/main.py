import requests
import json
import pandas as pd
import sqlite3

def extract():
    url="https://catfact.ninja/fact"
    try:
        response = requests.get(url)
        response.raise_for_status() 
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ 擷取數據時發生錯誤: {e}")
        return None
    else:
        print("--- 🔍 Data Profiling (數據探查) ---")
        print("1. Data Type (數據類型):", type(data))
        print("2. Pretty Structure (美化後的結構):\n", json.dumps(data, indent=2))
        print("------------------------------------")

        return data
    
def transform_data(raw_data):
    if not raw_data:
        return None
    facts = raw_data.get("fact","")
    current_time = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
    data_dict = {
        "timestamp": [current_time],
        "fact": [facts]
    }
    df = pd.DataFrame(data_dict) 
    return df

def load_fact_data(df):
    if df is None or df.empty:
        return
    
    conn = sqlite3.connect('cat_facts.db')
    df.to_sql(
        name='facts',
        con=conn,
        if_exists='append',
        index=False
    )
    conn.close()
    print(
        f"3/3 ✅  {len(df)} load into SQLite (`cat_facts.db` -> `facts`)！"
    )

if __name__ == "__main__":
    raw_data = extract()
    clean_df = transform_data(raw_data)
    load_fact_data(clean_df)
    print("🎉 ETL 管道完全成功通關！")

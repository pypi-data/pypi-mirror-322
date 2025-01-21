from president_speech.db.parquet_interpreter import read_parquet, get_parquet_full_path
import pandas as pd


def psearch_by_count():
    data_path = get_parquet_full_path()
    df = pd.read_parquet(data_path)
    
    while True:
        keyword = input ("검색할 키워드를 입력하세요(종료를 원하면 '종료하겠습니다'를 입력하세요)")
        if keyword == '종료하겠습니다':
            print ("종료합니다")
            break
        f_df = df[df['speech_text'].str.contains(str(keyword), case=False)]
        if not f_df.empty:
            rdf = f_df.groupby("president").size().reset_index(name="count").sort_values(by="count", ascending=False)
            sdf = rdf.sort_values(by='count', ascending=False).reset_index(drop=True)
            print(sdf.to_string(index=False))
        
        else:
            print("일치하는 값이 없습니다")
            continue 

def group_by_count():
    kw = "올림픽"
    data_path = get_parquet_full_path()
    df = pd.read_parquet(data_path)
    f_df = df[df['speech_text'].str.contains(str(kw), case=False)]
    rdf = f_df.groupby("president").size().reset_index(name="count").sort_values(by="count", ascending=False)
    sdf = rdf.sort_values(by='count', ascending=False).reset_index(drop=True)
    print(sdf.to_string(index=False))

from president_speech.db.parquet_interpreter import read_parquet, get_parquet_full_path
import pandas as pd
import typer


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

def group_by_count(keyword: str,asorde: bool,howmany: int):
    # TODO: ascending, 출력 rows size 이들의 변수 고려
    # pytest 코드 작성해보기
    # import this <- 해석해보세요
    data_path = get_parquet_full_path()
    df = pd.read_parquet(data_path)
    f_df = df[df['speech_text'].str.contains(keyword, case=False)]
    rdf = f_df.groupby("president").size().reset_index(name="count")
    sdf = rdf.sort_values(by='count', ascending=asorde).reset_index(drop=True)
    rdf = sdf.head(howmany)
    return rdf

def print_group_by_count(keyword: str,asorde: bool,howmany: int):
    rdf=group_by_count(keyword,asorde,howmany)
    print(rdf.to_string(index=False))


def entry_point():
    typer.run(print_group_by_count)

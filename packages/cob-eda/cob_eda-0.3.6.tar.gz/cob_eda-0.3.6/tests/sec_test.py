from cob_eda.cli import group_by_count
import pandas as pd

def test1():
    df=group_by_count("경제",False,5)
    assert isinstance(df, pd.DataFrame)
    assert df.iloc[0]["president"] == "문재인"
    assert len(df) == 5

def test_search_exception():
    row_count = 13
    df = group_by_count(keyword="자유", asorde=True, howmany=row_count)
    
    # assert
    assert isinstance(df, pd.DataFrame)
    assert len(df) < row_count

def test_정열_및_행수제한():
    # given
    row_count = 3
    is_asc = True

    # when
    df = group_by_count(keyword="자유", asorde=is_asc, howmany=row_count)
    
    # then
    assert isinstance(df, pd.DataFrame)
    assert df.iloc[0]["president"] == "윤보선"
    assert len(df) == row_count

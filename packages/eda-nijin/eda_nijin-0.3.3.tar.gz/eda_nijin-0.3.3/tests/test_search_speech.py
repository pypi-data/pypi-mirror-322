from eda_nijin.cli import group_by_count
import pandas as pd

def test_search_exception():
    row_count = 13
    df = group_by_count(keyword="자유", asc=True, rcnt=row_count)

    #assert
    assert isinstance(df, pd.DataFrame)
    assert len(df) < row_count

def test_정열_및_행수제한():
    #given
    row_count = 3
    is_asc = True

    #when
    df = group_by_count(keyword = "자유", asc=is_asc, rcnt=row_count)
    
    #then 
    assert isinstance(df, pd.DataFrame)
    assert df.iloc[0]["president"] == "윤보선"
    assert len(df) == row_count 

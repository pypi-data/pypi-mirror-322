from eda_ji.cli import group_by_count
import pandas as pd

def test_search():
    row_count = 13
    
    # When
    df = group_by_count(keyword="자유", ascen=True, n=row_count)
    # assert
    assert isinstance(df, pd.DataFrame) 
    assert len(df) < row_count

def test_search2():
    row_count = 3
    is_asc = True
    
    # When
    df = group_by_count(keyword="자유", ascen=is_asc, n=row_count)
    
    # assert
    assert isinstance(df, pd.DataFrame)
    assert df.iloc[0]["president"] == "윤보선"
    assert len(df) == row_count



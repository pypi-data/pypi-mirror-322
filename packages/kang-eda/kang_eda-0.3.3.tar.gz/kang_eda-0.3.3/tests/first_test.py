import pandas as pd
from kang_eda.cli import group_by_count

def test_first():
    row_count = 13
    df = group_by_count("자유", True, row = row_count)
    # None 값이 아닌지
    assert df is not None
    # assert len(df) == 3
    assert isinstance(df, pd.DataFrame)
    assert df.iloc[0]['president'] == '윤보선'
    assert len(df) < row_count
    # 빈 문자열이 아닌지
    #assert v != ""
    # 문자열에 문자도 있고, 숫자도 있는지
    #assert any(t.isalpha() for t in v)
    #assert any(t.isdigit() for t in v)
   #  assert all(df_desc['count'].iloc[i] >= df_desc['count'].iloc[i + 1] for i in range(len(df_desc) - 1)), "Data is not sorted in descending order"
    # assert all(df_asc['count'].iloc[i] <= df_asc['count'].iloc[i + 1] for i in range(len(df_asc) - 1)), "Data is not sorted in ascending order"
def test_정열_및_행수제한():
    # given
    row_count = 3
    is_asc = True

    # when
    df = group_by_count(keyword = "자유", asc = is_asc, row = row_count)

    # assert
    assert isinstance(df, pd.DataFrame)
    assert df.iloc[0]['president'] == '윤보선'
    assert len(df) == row_count

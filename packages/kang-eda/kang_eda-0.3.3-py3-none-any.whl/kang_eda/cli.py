from president_speech.db.parquet_interpreter import get_parquet_full_path
import pandas as pd
import typer

def group_by_count(keyword: str, asc: bool=False, row: int=12) -> pd.DataFrame:
    # TODO : ascending, 출력 rows size
    # pytest 코드를 만들어  볼까요
    # import this
    data_path = get_parquet_full_path()
    df = pd.read_parquet(data_path)
    fdf = df[df['speech_text'].str.contains(keyword, case = False)]
    gdf = fdf.groupby("president").size().reset_index(name = "count")
    sdf = gdf.sort_values(by='count', ascending = asc).reset_index(drop = True)
    
    if(row >12):
        row == 12
    rdf = sdf.head(row)
    return rdf

def print_group_by_count(keyword: str, asc: bool=False, row: int=12):
    rdf = group_by_count(keyword, asc, row)
    print(rdf.to_string(index = False))

def entry_point():
    typer.run(print_group_by_count)

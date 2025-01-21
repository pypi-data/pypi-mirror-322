from president_speech.db.parquet_interpreter import get_parquet_full_path
import pandas as pd
import typer

def group_by_count(keyword: str, asc: bool=False, rcnt: int=12) -> pd.DataFrame:
    data_path = get_parquet_full_path()
    df = pd.read_parquet(data_path)
    f_df = df[df['speech_text'].str.contains(keyword, case=False)]

    if f_df.empty:
        return None

    rdf = f_df.groupby('president').size().reset_index(name='count')
    sdf = rdf.sort_values(by='count', ascending=asc).reset_index(drop=True)
    cdf = sdf.head(rcnt)
    
    return cdf

def print_group_by_count(keyword: str, asc: bool=False, rcnt: int=12):
    df = group_by_count(keyword, asc, rcnt)
    if df is None:
        print("해당 데이터가 존재하지 않습니다.")
    else:
        print(df.to_string(index=False))

def entry_point():
    typer.run(print_group_by_count)

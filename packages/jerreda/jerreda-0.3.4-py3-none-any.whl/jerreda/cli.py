import typer
from president_speech.db.parquet_interpreter import get_parquet_full_path
import pandas as pd

def group_by_count(keyword: str) -> str:
    data_path = get_parquet_full_path()
    df = pd.read_parquet(data_path)
    f_df = df[df['speech_text'].str.contains(keyword, case=False)]

    if f_df.empty:
        return None

    rdf = f_df.groupby('president').size().reset_index(name='count')
    sdf = rdf.sort_values(by='count', ascending=False).reset_index(drop=True)
    result = sdf.to_string(index=False)
    
    print(result)
    return result

def entry_point(keyword: str = typer.Argument(..., help='검색 키워드')):
    group_by_count(keyword)

def main():
    typer.run(entry_point)

if __name__ == "__main__":
    typer.run(entry_point)

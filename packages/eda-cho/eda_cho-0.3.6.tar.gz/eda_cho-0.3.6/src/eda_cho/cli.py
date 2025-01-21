from president_speech.db.parquet_interpreter import get_parquet_full_path
import pandas as pd
import typer

def group_by_count(keyword: str, ascend: bool=False, rowsize: int=12)-> pd.DataFrame:
    data_path = get_parquet_full_path()
    df = pd.read_parquet(data_path)
    f_df = df[df['speech_text'].str.contains(keyword, case=False)]
    rdf = f_df.groupby("president").size().reset_index(name='count')
    sdf = rdf.sort_values(by='count', ascending=ascend).reset_index(drop=True)
    if(rowsize <= 0):
        sdf = sdf
    elif(rowsize > len(sdf)):
        sdf = sdf
    else:
        sdf = sdf[0:(rowsize)]
    return sdf

def print_group_by_count(keyword: str, ascend: bool=False, rowsize: int=12):
    df = group_by_count(keyword, ascend, rowsize)
    print(df.to_string(index=False))

def entry_point():
    typer.run(print_group_by_count)


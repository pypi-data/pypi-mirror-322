from president_speech.db.parquet_interpreter import get_parquet_full_path
import pandas as pd
data_path = get_parquet_full_path()

df = pd.read_parquet(data_path)




def group_by_count(a):
    f_df = df[df['speech_text'].str.contains(str(a), case=False)]
    rdf = f_df.groupby("president").size().reset_index(name='count')
    sdf = rdf.sort_values(by='count', ascending=False).reset_index(drop=True)
    return print(sdf)


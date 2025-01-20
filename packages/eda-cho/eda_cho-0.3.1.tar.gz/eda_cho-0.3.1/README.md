# eda-cho

### DEV
```bash
$ source .venv/bin/activate
$ pdm add pandas
$ pdm add -dG eda jupyterlab
$ pdm add <...>
$ pdm add -dG test pytest

```

### EDA
- run jupyterlab
```
$ jupyter lab

```


### REF
- [install jupyter](https://jupyter.org/install)
- from president_speech.db.parquet_interpreter import read_parquet, get_parquet_full_path
>>> get_parquet_full_path()
'/Users/f16/code/edu/president-speech/.venv/lib/python3.8/site-packages/president_speech/db/parquet/president_speech_ko.parquet'
>>> read_parquet().head(3)

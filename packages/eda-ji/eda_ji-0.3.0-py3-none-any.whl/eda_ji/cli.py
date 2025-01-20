from president_speech.db.parquet_interpreter import get_parquet_full_path
import pandas as pd


def group_by_count():
    kw = "올림픽"
    data_path = get_parquet_full_path()
    df = pd.read_parquet(data_path)
    fdf = df[df['speech_text'].str.contains("올림픽", regex=False)] # 올림픽 단어가 들어간 연설 df 만들
    gdf = fdf.groupby("president").size().reset_index(name="count")  # 대통령 별 개수 세서 그룹화 하기
    sdf = gdf.sort_values(by='count', ascending=False).reset_index(drop=True)  # 정렬 하기
    print(sdf.to_string(index=False))

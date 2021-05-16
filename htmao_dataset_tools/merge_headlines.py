import os
import pandas as pd

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
FILES_PATH = os.path.join(BASE_PATH, 'dataset')
OUTPUT_FILE = os.path.join(BASE_PATH, 'headlines/sa_guardian.csv')

paths = os.listdir(FILES_PATH)
paths.sort()

df = pd.DataFrame()
index = 0

for path in paths:
    print(path)
    df_part = pd.read_csv(os.path.join(FILES_PATH, path))

    for i, row in df_part.iterrows():
        df_part.at[i, 'ID'] = index
        index += 1

    df = df.append(df_part)


print(df)
df.to_csv(OUTPUT_FILE, index=False)
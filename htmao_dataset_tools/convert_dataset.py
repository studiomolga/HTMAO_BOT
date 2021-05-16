import os
import pandas as pd
import shutil

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
OUT_PATH = os.path.join(BASE_PATH, '../htmao_headlinalyser/headline_sentiment')
POS_PATH = os.path.join(OUT_PATH, 'train/pos')
NEUTRAL_PATH = os.path.join(OUT_PATH, 'train/neutral')
NEG_PATH = os.path.join(OUT_PATH, 'train/neg')
DATA_FILE = os.path.join(BASE_PATH, 'headlines/sa_guardian.csv')

# paths = [POS_PATH, NEUTRAL_PATH, NEG_PATH]

POS = 1
NEUTRAL = 0
NEG = -1

if not os.path.isdir(OUT_PATH):
    os.mkdir(OUT_PATH)
else:
    shutil.rmtree(OUT_PATH)
    os.mkdir(OUT_PATH)

os.makedirs(POS_PATH)
os.makedirs(NEUTRAL_PATH)
os.makedirs(NEG_PATH)

df = pd.read_csv(DATA_FILE)

pos_titles = []
neutral_titles = []
neg_titles = []

for i, row in df.iterrows():
    if row['LABEL'] == POS:
        pos_titles.append(row['TITLE'])
    elif row['LABEL'] == NEUTRAL:
        neutral_titles.append(row['TITLE'])
    elif row['LABEL'] == NEG:
        neg_titles.append(row['TITLE'])

titles = {POS_PATH: pos_titles, NEUTRAL_PATH: neutral_titles, NEG_PATH: neg_titles}

for path in titles:
    for i, title in enumerate(titles[path]):
        fn = '{}.txt'.format(i)
        fp = os.path.join(path, fn)
        with open(fp, 'w') as f:
            f.write(title)
        print(i, path, title)

# print(len(pos_titles))
# print(len(neg_titles))
# print(len(neutral_titles))

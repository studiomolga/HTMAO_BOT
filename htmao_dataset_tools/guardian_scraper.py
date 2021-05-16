import requests
from bs4 import BeautifulSoup
from time import sleep
import os
import pandas as pd

PAGE = 'https://www.theguardian.com/environment/climate-change?page={}'
PAGE_FROM = 41          #start page
PAGE_TO = 200           #end page
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = os.path.join(BASE_PATH, 'headlines/guardian02.csv')


def main():
    id = 1
    df = pd.DataFrame(columns=['ID', 'TITLE'])
    for page in range(PAGE_FROM, PAGE_TO):
        page = requests.get(PAGE.format(page))
        soup = BeautifulSoup(page.content, 'html.parser')
        for tag in soup.findAll('h3', class_='fc-item__title'):
            title = tag.find('span', class_='js-headline-text').get_text()
            new_row = {'ID': id, 'TITLE': title}
            print('adding new row to dataset:\n {}\n'.format(new_row))
            df = df.append(new_row, ignore_index=True)
            id += 1
        sleep(1)

    print('saving file as: {}'.format(OUTPUT_FILE))
    df.to_csv(OUTPUT_FILE, index=False)


if __name__ == '__main__':
    main()

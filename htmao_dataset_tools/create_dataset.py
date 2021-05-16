import os
import pandas as pd

FILE_AMOUNT = 100
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(BASE_PATH, 'headlines/guardian01.csv')
OUTPUT_FILE = os.path.join(BASE_PATH, 'headlines/sa_guardian.csv')


def main():
    csv_file = pd.read_csv(INPUT_FILE)
    # csv_size = csv_file.shape[0] - 1
    # frac = float(FILE_AMOUNT) / float(csv_size)
    # subset = csv_file.sample(frac=frac)

    if os.path.isfile(OUTPUT_FILE):
        output_df = pd.read_csv(OUTPUT_FILE)
    else:
        output_df = pd.DataFrame(columns=['ID', 'TITLE', 'LABEL'])

    index = 0
    for _, row in csv_file.iterrows():
        print(row['ID'])
        # print(row['ID'] not in output_df['ID'].to_list(), row['ID'], row['TITLE'])
        # print(output_df.ID)
        if row['TITLE'] not in output_df['TITLE'].to_list():
            new_row = {'ID': int(row['ID']), 'TITLE': str(row['TITLE'])}
            # print(f'index: {index} \ntitle: {new_row["TITLE"]}')
            print 'index: %d\ntitle: %s' % (index, new_row["TITLE"])
            label = raw_input('enter sentiment (-1 = neg, 0 = neutral, 1 = pos, q to stop: ')
            # print()
            print '\n'


            if str(label) == 'q':
                break
            elif int(label) == -1 or int(label) == 0 or int(label) == 1:
                new_row['LABEL'] = int(label)
                output_df = output_df.append(new_row, ignore_index=True)
                index += 1
                output_df.to_csv(OUTPUT_FILE, index=False)

    output_df.to_csv(OUTPUT_FILE, index=False)


if __name__ == '__main__':
    main()

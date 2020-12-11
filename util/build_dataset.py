#Core
import math
import os
from shutil import copy2

# External
import pandas as pd


def split_csv():
    df = pd.read_csv('speech_data.csv', dtype={'wav_filename': 'string', 'wav_filesize': int, 'transcript': 'string'}, index_col=0)

    total_size = len(df)
    train_size = math.floor(.8 * total_size)

    # 
    train = df.head(train_size)

    test_dev_size = total_size - train_size

    try:
        os.mkdir('training_csvs')
    except:
        pass

    #
    test_dev = df.tail(test_dev_size)
    test_dev.to_csv('training_csvs/test_dev.csv')

    tdf = pd.read_csv('training_csvs/test_dev.csv', dtype={'wav_filename': 'string', 'wav_filesize': int, 'transcript': 'string'}, index_col=0)

    total_size = len(tdf)
    test_size = math.floor(.5 * total_size)

    #
    test = tdf.head(test_size)
    dev = tdf.tail(total_size - test_size)
    dev.to_csv('training_csvs/dev.csv')
    dev = pd.read_csv('training_csvs/dev.csv', index_col=0)

    #
    os.remove('training_csvs/test_dev.csv')

    # Saving
    train.to_csv('training_csvs/train.csv')
    test.to_csv('training_csvs/test.csv')
    dev.to_csv('training_csvs/dev.csv')

def strip_sounds(directory='test'):
    try:
        os.mkdir('training_csvs')
    except:
        pass

    for root, dirs, files in os.walk(directory):
        for f in files:
            titles = f.split('-')
            if f.find('__chunk__') != -1 and f.find('.wav') != -1 and len(titles) == 5:
                print(os.path.join(root, f))
                copy2(os.path.join(root, f), os.path.join(os.getcwd(), 'training_csvs'))

# split_csv()
# strip_sounds(directory='wazobia')

if __name__ == '__main__':
    split_csv()
    # print('hello_2')

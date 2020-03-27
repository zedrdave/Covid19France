#!/usr/bin/python3

import pandas as pd
import numpy as np
import glob

FROM_YEAR = 2015
COMBINE_YEARS = False

data_path = './data'
csv_path = './csv'

fields = {
    'acte': (167, 176),
    'sex': (80, 81),
    'birthyear': (81, 85),
    'date': (154, 162),
    'place': (162, 164)
    }
# place == 99 -> abroad

columns = ['year', *fields.keys()]

for filepath in glob.glob(f'{data_path}/*.txt'):
    rows = []
    filename = filepath.split('/')[-1]
    with open(f'{data_path}/{filename}') as f:
        year = int(filename[6:10])
        if year < FROM_YEAR:
            continue

        print(f"{year}: {filename}")
        for l in f:
            try:
                cols = { k:l[slice(*v)].strip() for k,v in fields.items() }
                if cols['place'] == '':
                    cols['place'] = 0
                elif cols['place'][1] in ('A', 'B'): # Corsica
                    cols['place'] = cols['place'][0]
                cols['year'] = year
                rows.append([cols[k] if k == 'acte' else int(cols[k]) for k in columns])

            except Exception as e:
                print(e)
                print(l)
                print({ k:l[slice(*v)].strip() for k,v in fields.items() })
                raise e
            # if len(rows) > 10000:
            #     break

    df  = pd.DataFrame(rows, columns = columns)
    df.set_index(['year', 'acte'])
    df['acte'] = df['acte'].astype(str)
    print(df.shape)
    # print(df.dtypes)

    if COMBINE_YEARS:
        csv_name = f'{csv_path}/all_years.csv'
    else:
        csv_name = f'{csv_path}/{year}.csv'
    with open(csv_name, 'a') as f:
        df.to_csv(f, header=f.tell()==0)

import pandas
from argparse import ArgumentParser
import os
import json
import shared
import numpy as np
import math
import numbers

parser = ArgumentParser()
parser.add_argument('file')
parser.add_argument('--sheet-name', default=0)
parser.add_argument('--filter') # Example 0=Value,1=Test
args = parser.parse_args()

if not os.path.exists(args.file):
    print('File does not exist')
    exit()


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, np.bool_):
            return bool(obj)
        else:
            return super(NpEncoder, self).default(obj)

sheet_name = int(args.sheet_name) if args.sheet_name.isnumeric() else args.sheet_name
sheet = pandas.read_excel(args.file, sheet_name=sheet_name)
OUTPUT = shared.output_dir(__file__)
FILE = OUTPUT + '/result.json'

filter_values = {}
if args.filter:
    for pair in args.filter.split(','):
        split = pair.split('=')
        if split[0].isnumeric():
            idx = int(split[0])
            if idx >= 0 and idx < len(sheet.columns):
                col_name = sheet.columns[idx]
                filter_values[col_name] = split[1]

with open(FILE, 'w') as f:
    all_result = []
    for rowIdx in range(0, sheet.index.stop):
        row = sheet.loc[rowIdx]
        result = {}

        filtered = False
        for col in row.index:
            value = row[col]
            if isinstance(value, numbers.Number) and math.isnan(value):
                value = ""

            if col in filter_values:
                filter_value = filter_values[col]

                if filter_value and value != filter_value:
                    filtered = True

            result[col] = value

        if filtered: continue

        all_result.append(result)

    f.write(json.dumps(all_result, cls=NpEncoder))
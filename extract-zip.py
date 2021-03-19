from zipfile import ZipFile
import argparse
import shared

parser = argparse.ArgumentParser()
parser.add_argument('zip_file')
parser.add_argument('filename')
parser.add_argument('-m', '--match', default='exact',
                    choices=['exact', 'starts_with', 'ends_with'])
parser.add_argument('--unzip', default=False, action='store_true')
args = parser.parse_args()

OUTPUT = shared.output_dir(__file__)
filename = args.filename
match = args.match

with ZipFile(args.zip_file, 'r') as zfile:
    for name in zfile.namelist():
        if (match == 'exact' and name == filename) or \
            (match == 'starts_with' and name.startswith(filename)) or \
                (match == 'ends_with' and name.endswith(filename)):
                print(f'Extracting file {name}')
                name_only = name.split('.')[0]
                zfile.extract(name, path=OUTPUT)
                if args.unzip:
                    with ZipFile(OUTPUT + '/' + name, 'r') as innerZip:
                        innerZip.extractall(OUTPUT + '/' + name_only)

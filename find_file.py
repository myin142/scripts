import os
import sys
from argparse import ArgumentParser
from shared import Colors, color

parser = ArgumentParser()
parser.add_argument('folder')
parser.add_argument('text')
parser.add_argument('--match-file-name', default=False, action='store_true')
parser.add_argument('--snippet-size', default=40, type=int)
parser.add_argument('--recursive', default=False, action='store_true') # TODO
args = parser.parse_args()


FOLDER = args.folder
txt = args.text
snippet_size = args.snippet_size

files = {}
for filename in os.listdir(FOLDER):
    path = os.path.join(FOLDER, filename)
    if os.path.isfile(path):
        if args.match_file_name:
            if txt in filename:
                files[filename] = ''
        else:
            with open(path, 'r') as f:
                content = f.read()
                if txt in content:
                    # TODO: display multiple matches in a single file
                    match_index = content.index(txt)
                    start = match_index - snippet_size
                    end = match_index + len(txt) + snippet_size
                    files[filename] = content[start:end].replace(
                        txt, color(txt, Colors.FAIL))

print('Searched folder {} for text "{}"'.format(FOLDER, txt))
for f in files:
    print(color(f + ':', Colors.HEADER))
    print(files[f])

print(color(f'\nFound in {len(files)} files', Colors.OKGREEN))

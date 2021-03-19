import os
import sys
from shared import Colors, color

# Arg 1: folder to search
# Arg 2: text to search

if len(sys.argv) < 3:
    print('Missing arguments')
    exit()

FOLDER = sys.argv[1]
txt = sys.argv[2]
SNIPPET_SIZE = 40

files = {}
for filename in os.listdir(FOLDER):
    path = os.path.join(FOLDER, filename)
    if os.path.isfile(path):
        with open(path, 'r') as f:
            content = f.read()
            if txt in content:
                # TODO: display multiple matches in a single file
                match_index = content.index(txt)
                start = match_index - SNIPPET_SIZE
                end = match_index + len(txt) + SNIPPET_SIZE
                files[filename] = content[start:end].replace(txt, color(txt, Colors.FAIL))

print('Searched folder {} for text "{}"'.format(FOLDER, txt))
for f in files:
    print(color(f + ':', Colors.HEADER))
    print(files[f])

print(color(f'\nFound in {len(files)} files', Colors.OKGREEN))
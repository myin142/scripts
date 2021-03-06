import os
import sys
from argparse import ArgumentParser
from shared import Colors, color

parser = ArgumentParser()
parser.add_argument('folder')
parser.add_argument('--filename')
parser.add_argument('--content')
parser.add_argument('--snippet-size', default=40, type=int)
parser.add_argument('-d', '--depth', default=1, type=int)
parser.add_argument('-v', '--verbose', default=False, action='store_true')
args = parser.parse_args()


FOLDER = args.folder
txt = args.content
snippet_size = args.snippet_size
max_depth = args.depth

files = {}


def search_in_folder(dir, depth=1):
    files[dir] = {}

    if args.verbose:
        print(f'Search in directory {dir}')

    for filename in os.listdir(dir):
        path = os.path.join(dir, filename)
        if os.path.isfile(path):
            if args.filename:
                if args.filename in filename:
                    files[dir][filename] = ''
            else:
                with open(path, 'r') as f:
                    try:
                        content = f.read()
                        if txt in content:
                            # TODO: display multiple matches in a single file
                            match_index = content.index(txt)
                            start = match_index - snippet_size
                            end = match_index + len(txt) + snippet_size
                            files[dir][filename] = content[start:end].replace(
                                txt, color(txt, Colors.FAIL))
                    except:
                        if args.verbose:
                            print(f'Failed to read content of file {path}')

        elif (max_depth == -1 or depth < max_depth) and os.path.isdir(path):
            search_in_folder(path, depth + 1)


if args.verbose:
    print(f'Searching for text "{txt}"')
search_in_folder(FOLDER)

count = 0
for dir in files:
    for f in files[dir]:
        count += 1
        path = os.path.join(dir, f)
        print(color(path + ':', Colors.HEADER))
        print(files[dir][f])

print(color(f'\nFound in {count} files', Colors.OKGREEN))

from zipfile import ZipFile
from io import BytesIO
import argparse
import shared

parser = argparse.ArgumentParser(description='Extract zips inside a zip, either by filename or specific contents')
parser.add_argument('zip_file')
parser.add_argument('-f', '--filename', help='Find zip file by filename')
parser.add_argument('--content', nargs='+', default=[], help='Find files for all contents in one of the zip files')
parser.add_argument('--match-all', default=False, action='store_true', help='All content has to match in a file')
parser.add_argument('--find-all', default=False, action='store_true', help='Find all matches')
parser.add_argument('--file-match', default='exact',
                    choices=['exact', 'starts_with', 'ends_with'], help='How to match file name')
parser.add_argument('--unzip', default=False, action='store_true')
args = parser.parse_args()

OUTPUT = shared.output_dir(__file__)
filename = args.filename
match = args.file_match
content_search = len(args.content) > 0
contents = args.content
find_one = not args.find_all
match_all = args.match_all

def extract(zip, name):
    print(f'Extracting file {name}')
    name_only = name.split('.')[0]
    zfile.extract(name, path=OUTPUT)
    if args.unzip:
        with ZipFile(OUTPUT + '/' + name, 'r') as innerZip:
            innerZip.extractall(OUTPUT + '/' + name_only)

def contains_any_content(value: str) -> str:
    found = []
    for search in contents:
        if search in value:
            found.append(search)
    return found

def contains_all_content(v: str) -> bool:
    for search in contents:
        if not search in v:
            return False
    return True

print(f'Search in {args.zip_file} for {filename} / {args.content}')

files = []
found_content = []

with ZipFile(args.zip_file, 'r') as zfile:
    for name in zfile.namelist():
        if content_search:
            zfiledata = BytesIO(zfile.read(name))
            with ZipFile(zfiledata) as innerZip:
                for inner_name in innerZip.namelist():
                    content = innerZip.read(inner_name).decode('utf-8')
                    if match_all:
                        if contains_all_content(content):
                            files.append(name)
                            if find_one:
                                contents = []
                            break
                    else:
                        found = contains_any_content(content)
                        if len(found):
                            for search in found:
                                if not search in found_content:
                                    found_content.append(search)
                                if find_one:
                                    contents.remove(search)
                            files.append(name)

            if len(contents) == 0:
                break
        else:
            if (match == 'exact' and name == filename) or \
                (match == 'starts_with' and name.startswith(filename)) or \
                    (match == 'ends_with' and name.endswith(filename)):
                        files.append(name)
                        if find_one:
                            break

    for f in files:
        extract(zfile, f)
    
    not_found = [c for c in contents if not c in found_content]
    if len(not_found) > 0 and content_search:
        print(f'Not found content {not_found}')

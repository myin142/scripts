import os
import sys

# Arg 1: folder to search
# Arg 2: text to search

if len(sys.argv) < 3:
    print('Missing arguments')
    exit()

FOLDER = sys.argv[1]
txt = sys.argv[2]

files = []
for filename in os.listdir(FOLDER):
    path = os.path.join(FOLDER, filename)
    if os.path.isfile(path):
        with open(path, 'r') as f:
            if txt in f.read():
                files.append(filename)

print(files)

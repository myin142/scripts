import json
import requests
import os
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('manifest')
parser.add_argument('--output', default='output/forge-mods')
args = parser.parse_args()

file = args.manifest
output = args.output

if not os.path.exists(output):
    os.makedirs(output)

with open(file, 'r') as f:
    manifest = json.loads(f.read())

    if not manifest['files']:
        exit()

    for mod in manifest['files']:
        info_url = f'https://cursemeta.dries007.net/{mod["projectID"]}/{mod["fileID"]}.json'
        print(f'Getting info {info_url}')
        info_response = requests.get(info_url)

        if info_response.status_code == 200:
            info = info_response.json()
            print(f'Downloading {info["DisplayName"]}')
            response = requests.get(info['DownloadURL'])

            with open(output + '/' + info['FileName'], 'wb') as out:
                out.write(response.content)
        else:
            print(
                f'Failed to get info {info_response.status_code}. {info_response.text}')

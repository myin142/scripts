import json
import re 
import requests 
from bs4 import BeautifulSoup 
import os.path

PATH = "holo_originals.html"
OUTPUT = "holo_originals.json"
URL = "https://seesaawiki.jp/hololivetv/d/%a5%aa%a5%ea%a5%b8%a5%ca%a5%eb%a5%bd%a5%f3%a5%b0"
# URL = "https://seesaawiki.jp/hololivetv/d/%a5%aa%a5%ea%a5%b8%a5%ca%a5%eb%a5%bd%a5%f3%a5%b0"
  
def load_content():
    r = requests.get(URL) 
    if r.status_code == 200:
        with open(PATH, "w") as file:
            file.write(r.text)

if not os.path.isfile(PATH):
    load_content()

data = {}
count = 0

multiple = []
  
with open(PATH, "r") as file:
    soup = BeautifulSoup(file.read(), 'html.parser') 
    table = soup.find("table", {"id": "content_block_14"})
    rows = table.find_all("tr")
    print(f'Found {len(rows)} items')

    for row in rows:
        cols = row.find_all("td")
        if len(cols) == 0: continue

        date = cols[0].text.strip()
        names = [n.strip() for n in cols[1].text.split(',')]
        song = cols[2].text

        link = cols[2].find("img")['src']
        match = re.search("vi/([a-zA-Z0-9_-]+)", link)
        if match == None:
            print(f"No match found for {song}: {link}")

        id = match.groups()[0] if match != None else ""

        if len(names) > 1:
            multiple.append(names)
            # print(f"Skipping multiple members for now. {names}")
            continue

        name = ','.join(names) #.replace('’', '').replace('\'', '')
        if not name in data:
            data[name] = []

        data[name].append({"song": song, "date": date, "id": id})

        # count += 1
        # if count > 22:
        #     break

print(f'In total {len(data)} members')
for name in data:
    print(f'{name} has {len(data[name])} songs')

for s in data['博衣こより']:
    print(s)

with open(OUTPUT, 'w') as out:
    json.dump(data, out)

# for n in multiple:
#     print(n)
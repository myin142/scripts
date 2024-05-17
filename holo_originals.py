import json
import re 
import requests 
from bs4 import BeautifulSoup 
import os.path, os
from dotenv import load_dotenv
import base64
import subprocess
import yt_dlp
import time

PATH = "holo_originals.html"
OUTPUT = 'output/holo_originals'
URL = "https://seesaawiki.jp/hololivetv/d/%a5%aa%a5%ea%a5%b8%a5%ca%a5%eb%a5%bd%a5%f3%a5%b0"
# URL = "https://seesaawiki.jp/hololivetv/d/%a5%aa%a5%ea%a5%b8%a5%ca%a5%eb%a5%bd%a5%f3%a5%b0"

def get_spotify_token():
    load_dotenv()
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")

    auth_string = f'{client_id}:{client_secret}'.encode('utf-8')
    auth_base64 = str(base64.b64encode(auth_string), 'utf-8')

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": f"Basic {auth_base64}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}

    res = requests.post(url, data=data, headers=headers)
    json_res = json.loads(res.content)
    return json_res['access_token']
  
def load_content():
    r = requests.get(URL) 
    if r.status_code == 200:
        with open(PATH, "w") as file:
            file.write(r.text)

if not os.path.isfile(PATH):
    load_content()

if not os.path.isdir(OUTPUT):
    os.mkdir(OUTPUT)
# token = get_spotify_token()
# print(token)

def create_data():
    data = {}
    count = 0

    multiple = []
    
    with open(PATH, "r") as file:
        soup = BeautifulSoup(file.read(), 'html.parser') 
        # table = soup.find("table", {"id": "content_block_14"})
        # rows = table.find_all("tr")

        container = soup.find("div", {"class": "user-area"})
        rows = container.find_all("div", {"class": "wiki-section-3"})

        for row in rows:
            # cols = row.find_all("td")
            # if len(cols) == 0: continue

            # date = cols[0].text.strip()
            # full_name = cols[1].text
            # names = [n.strip() for n in full_name.split(',')]
            # song = cols[2].text

            # link = cols[2].find("img")['src']
            # match = re.search("vi/([a-zA-Z0-9_-]+)", link)
            # if match == None:
            #     print(f"No match found for {song}: {link}")

            # id = match.groups()[0] if match != None else ""

            date = ""
            full_name = ""
            names = []
            song = row.find("h5").text.strip()
            id = ""

            body = row.find("div", {"class": "wiki-section-body-3"})
            lines = body.text.split('\n')

            for line in lines:
                if '公開日' in line:
                    parts = line.split('：')
                    date = parts[1].strip()
                elif 'メンバー' in line:
                    parts = line.split('：')
                    if len(parts) == 1:
                        parts = line.split(':')

                    full_name = parts[1].strip()
                    for n in full_name.split(','):
                        for x in n.split('、'):
                            names.append(x.strip())
            
            links = [x for x in row.find_all("a") if 'youtube' in x.text.lower()]
            if len(links) > 0:
                a = [l for l in links if '(mv)' in l.text.lower()]
                if len(a) == 0:
                    a = links[0]
                else:
                    a = a[0]

                link = a['href']
                match = None
                if 'watch?v=' in link:
                    # https://www.youtube.com/watch?v=cU5_JIEFTOw
                    match = re.search("v=([a-zA-Z0-9_-]+)", link)
                elif 'tu.be' in link:
                    # https://youtu.be/7WXVFl-N6-o
                    # https://youtu.be/6rHKnVVp8QQ?si=JNOpnNyezv9nTPBV
                    match = re.search("be/([a-zA-Z0-9_-]+)\\??", link)

                if match == None:
                    print(f"No match found for {song}: {a.text}, {link}")
                else:
                    id = match.groups()[0]

            if 'remix' in song.lower() or 'ver.' in song.lower() or 'Renovation' in song:
                continue

            if len(names) > 1:
                if 'FUWAMOCO' in full_name:
                    names = ['FUWAMOCO']
                else:
                    multiple.append(names)
                    # print(f"Skipping multiple members for now. {names}")
                    continue

            name = ','.join(names) #.replace('’', '').replace('\'', '')
            name = name.split('/')[0]
            name = name.replace('Pavolla', 'Pavolia')
            name = name.replace('kanaeru', 'Kanaeru')
            
            match = re.search('\\(.*\\)', name)
            if match != None:
                continue

            if not name in data:
                data[name] = []

            data[name].append({"song": song, "date": date, "id": id})

            # count += 1
            # if count > 22:
            #     break

    print(f'In total {len(data)} members')
    # for name in data:
    #     print(f'{name} has {len(data[name])} songs')

    for name in data:
        for song in data[name]:
            id = song["id"]
            if id:
                try:
                    with yt_dlp.YoutubeDL({'outtmpl': f'{OUTPUT}/{id}.%(ext)s', 'format': 'bestaudio/best'}) as ydl:
                        ydl.download(id)
                except:
                    print(f'Failed to download video {id}')

                time.sleep(1)

    # with open("holo_originals.txt", 'w') as out:
    #     for name in data:
    #         out.write(f'--{name}\n')
    #         for x in data[name]:
    #             out.write(f'{x["date"]};{x["song"]};{x["id"]}\n')
    #         out.write('\n')
    
    # with open('holo_names.txt', 'w') as names:
    #     for name in sorted(data.keys()):
    #         names.write(f'{name}\n')

# create_data()

def to_ogg():
    if not os.path.exists(f'{OUTPUT}/ogg'):
        os.mkdir(f'{OUTPUT}/ogg')

    for file in os.listdir(OUTPUT):
        file_name = file.split('.')
        proc = subprocess.Popen(['ffmpeg', '-i', f'{OUTPUT}/{file}', '-vn', '-acodec', 'libvorbis', f'{OUTPUT}/ogg/{file_name[0]}.ogg', '-n'])
        proc.wait()
        print(f'File {file} has been converted: {proc.returncode}')

to_ogg()
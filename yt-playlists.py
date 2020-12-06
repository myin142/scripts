import youtube_dl

# Download from terminal directly
# youtube-dl --extract-audio --audio-format mp3 -o "%(title)s.%(ext)s" <url to playlist>

playlists = {
    # "13": "PLhVmt2W2Ji9Ic_xK-b0uKMadGeXN-Tg18",
    # "12": "PLhVmt2W2Ji9IzwdYKAXeKH-rpWgzBsrIO",
    # "11": "PLhVmt2W2Ji9JPK2AWMh97RZMtF5NA0tRl",
    # "10": "PLhVmt2W2Ji9KomaAEfiERissSk1WFWfnh",
    # "9": "PLhVmt2W2Ji9K7AeodnTLwqxzj3hj_lHp3",
    # "8": "PLhVmt2W2Ji9Km4A3vOkDWyRrWakvgT_7I",
    # "7": "PLhVmt2W2Ji9LwNQyoBf9oDAKaqKhI7yUz",
    # "6": "PLhVmt2W2Ji9LRh-ERWb3InLkPScF_46pX",
    # "5": "PLhVmt2W2Ji9Kn9eDZnEmmGrAxvupUgoGQ",
    # "4": "PLhVmt2W2Ji9KNm02_KGn4G4NPq8Vu_t7z",
    # "3": "PLhVmt2W2Ji9J-518UjsG9Fw68moSIJXn4",
    # "2": "PLhVmt2W2Ji9IRsWIqy_b0EpOZjdpq64gz",
    # "1": "PLhVmt2W2Ji9KsySfgTui1TFUN6JBzILbn",
}

opt = {
    'format': 'bestaudio/best',
    'cachedir': 'youtube',
    'post_processors': [
        {
            'key': 'FFmpegExtractAudioPP',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        },
    ],
}

for k in playlists.keys():
    opt['outtmpl'] = 'youtube/' + k + '/' + '%(title)s.%(ext)s'
    with youtube_dl.YoutubeDL(opt) as ydl:
        ydl.download([playlists[k]])
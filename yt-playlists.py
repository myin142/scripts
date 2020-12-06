import youtube_dl

# Download from terminal directly
# youtube-dl --extract-audio --audio-format mp3 -o "%(title)s.%(ext)s" <url to playlist>

playlists = [
    #"PLhVmt2W2Ji9Ic_xK-b0uKMadGeXN-Tg18"
    "PLhVmt2W2Ji9KNm02_KGn4G4NPq8Vu_t7z"
]

opt = {
    'outtmpl': '%(title)s.%(ext)s',
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

with youtube_dl.YoutubeDL(opt) as ydl:
    ydl.download(playlists)
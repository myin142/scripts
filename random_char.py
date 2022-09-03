import random
import requests as req


def get_anime_info(anime_id: int):
    res = req.get(f'https://www.animecharactersdatabase.com/api_series_characters.php?anime_id={anime_id}', headers={'User-Agent': 'random-character-script:v0.0.1'})
    res.raise_for_status()
    return res.json()

def print_random_character(data):
    characters = data['characters']
    character = random.choice(characters)

    anime = data['anime_name']
    name = character['name']
    character_id = character['id']

    print(f'{name} from {anime}')
    print(f'https://www.animecharactersdatabase.com/characters.php?id={character_id}')


animes = [
    106980, # Hololive
    108305, # Spy x Family
    106225, # Kaguya
    106339, # Kimetsu
    107496, # Mushoku
    100135, # Vocaloid
    106146, # Gotoubun
    107379, # Genshin
    105402, # LoL
]
anime_id = random.choice(animes)
info = get_anime_info(anime_id)
print_random_character(info)
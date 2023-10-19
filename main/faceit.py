import requests
from database.postgresql import pcursor

API_KEY = '51fa23e3-950d-4a71-9d92-907c2cd76845'

header = {'accept': 'application/json', 'Authorization': f'Bearer {API_KEY}'}
url = 'https://open.faceit.com/data/v4'


def faceit_get_player_elo(user: int, steamid: int):
    response = requests.get(
        url + f'/players?game=csgo&game_player_id={steamid}', headers=header)

    try:
        level = response.json()['games']['cs2']['skill_level']
        elo = response.json()['games']['cs2']['faceit_elo']

        pcursor.execute(
            "UPDATE connections SET faceitlvl = %s, faceitelo = %s WHERE user_id = %s",
            (level, elo, user)
        )
        return level
    except KeyError:
        return None

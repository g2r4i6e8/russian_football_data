import os

import pandas as pd
import requests
from bs4 import BeautifulSoup
import tqdm
import pickle
from selenium.webdriver.support.ui import WebDriverWait
import random

from scripts.utils import ProxyRotator, setup_driver, parse_base_info, parse_career, get_season_map, parse_season


def collect_player_urls():
    base_url = 'https://premierliga.ru/players/?cur_cc=1&season=all&club=all&position=all&fdo=all&letter=all&curPos={}'

    player_urls = []
    pbar = tqdm.tqdm()
    for i in range(0,10**6):
        target_url = base_url.format(i*20)
        response = requests.get(target_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        player_list = soup.find_all("tr", {"class": "player"})
        if len(player_list) < 1:
            break
        for player in player_list:
            player_href = player.find('a').get('href')
            player_urls.append(player_href)
        pbar.update(1)
    pbar.close()

    with open(os.pardir,'raw_data','player_urls.pickle', 'wb') as handle:
        pickle.dump(player_urls, handle)

def collect_player_data(player_urls, serialize=True):
    players = []
    errors = []
    pbar = tqdm.tqdm(player_urls)
    proxy_rotator = ProxyRotator()
    proxy = proxy_rotator.get_random_proxy()
    driver = setup_driver(proxy)
    for n, player_url in enumerate(player_urls):

        if n % 300 == 0:
            num_of_players = len(players)
            if num_of_players > 0:
                print(f'\nDumping players to a file. Number of players: {num_of_players}')
                with open(os.path.join(os.pardir,'raw_data','players_raw.pickle'), 'wb') as handle:
                    pickle.dump(players, handle)
        try:
            base_url = f'https://premierliga.ru/{player_url}'
            url = f'{base_url}'
            driver.get(url)
            WebDriverWait(driver, random.randint(1, 7))

            # response = requests.get(f'https://premierliga.ru/{player_url}')
            soup = BeautifulSoup(driver.page_source, 'html.parser')
        except Exception as e:
            print(f'\nError while getting request about player {player_url}: {e}\nPlayer will not be created')
            errors.append((player_url, 'request'))
            continue
        try:
            name = soup.find("div", {"class": "player-title"}).find("h1", {"class": "name"}).text.strip()
        except Exception as e:
            print(f'\nError while getting name of the player {player_url}: {e}\nPlayer will not be created')
            errors.append((player_url, 'name'))
            continue
        try:
            base_info = soup.find('figcaption').find_all('span')
            player = parse_base_info(name, base_info)
        except Exception as e:
            print(f'\nError while getting base info about player {player_url}: {e}\nPlayer will not be created')
            errors.append((player_url, 'base info'))
        try:
            career_info = soup.find_all("table", {"class": "transfers"})
            player.career = parse_career(career_info)
        except Exception as e:
            # print(f'\nError while getting career info of the player {player_url}: {e}')
            errors.append((player_url, 'career info'))

        try:
            season_info = soup.find_all("div", {"class": "season"})
            seasons_map = get_season_map(season_info)
            season_matches = soup.find_all("div", {"class": "player-table-stats"})
            player_matches = []
            for season in season_matches:
                season_id = season.get('rel')
                season_year = seasons_map[season_id]
                player_matches.extend(parse_season(season_year, season))
            player.matches = player_matches
        except Exception as e:
            # print(f'\nError while getting seasonal info of the player {player_url}: {e}')
            errors.append((player_url, 'seasonal info'))

        players.append(player)
        pbar.update(1)
    pbar.close()
    driver.close()

    if serialize:
        print(f'\nDumping players to a file. Number of players: {len(players)}')
        with open(os.path.join(os.pardir,'raw_data','players_raw.pickle'), 'wb') as handle:
            pickle.dump(players, handle)

        with open(os.path.join(os.pardir,'raw_data','errors.pickle'), 'wb') as handle:
            pickle.dump(errors, handle)
    else:
        return players, errors


def serialize_data():
    with open(os.path.join(os.pardir,'raw_data','players_raw.pickle'), 'rb') as handle:
        players = pickle.load(handle)

    players_list = []
    career_list = []
    matches_list = []

    for player in players:
        player_data, career_data, matches_data = player.serialize()
        players_list.append(player_data)
        career_list.extend(career_data)
        matches_list.extend(matches_data)

    for name, data in [('players', players_list), ('matches', matches_list), ('careers', career_list)]:
        pd.DataFrame(data).to_csv(os.path.join(os.pardir,'data', f'{name}.csv.gz'), index=False, compression='gzip')
import os

import pandas as pd
import uuid
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import random


class ProxyRotator:
    def __init__(self):
        with open(os.path.join(os.pardir,'resources','proxies.txt'), 'r') as f:
            self.proxies = [line.strip() for line in f]

    def get_random_proxy(self):
        return random.choice(self.proxies)


def setup_driver(proxy):
    opts = Options()
    opts.add_argument(f'--proxy-server={proxy}')
    opts.add_argument(
        "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36")
    driver = webdriver.Firefox(options=opts)
    return driver


class Match():
    def __init__(self, season, tournament, date, match, result, minutes, goals, scored_penalties, unscored_penalties,
                 yellow_card, yellow_red_card, red_card):
        self.season = season
        self.tournament = tournament
        self.date = date
        self.match = match
        self.result = result
        self.minutes = minutes
        self.goals = goals
        self.scored_penalties = scored_penalties
        self.unscored_penalties = unscored_penalties
        self.yellow_card = yellow_card
        self.yellow_red_card = yellow_red_card
        self.red_card = red_card

    def serialize(self, uid):
        return {
            'uid': uid,
            'season': self.season,
            'tournament': self.tournament,
            'date': self.date,
            'match': self.match,
            'result': self.result,
            'minutes': self.minutes,
            'goals': self.goals,
            'scored_penalties': self.scored_penalties,
            'unscored_penalties': self.unscored_penalties,
            'yellow_card': self.yellow_card,
            'yellow_red_card': self.yellow_red_card,
            'red_card': self.red_card
        }


class Player():
    def __init__(self, name, date_of_birth, citizenship, height, weight):
        self.name = name
        self.date_of_birth = date_of_birth
        self.citizenship = citizenship
        self.height = height
        self.weight = weight

        career = list()
        matches = list()

    def serialize(self):
        uid = uuid.uuid4().hex
        player_data = {
            'uid': uid,
            'name': self.name,
            'date_of_birth': self.date_of_birth,
            'citizenship': self.citizenship,
            'height': self.height,
            'weight': self.weight
        }
        career_data = []
        try:
            career_data = [{'uid': uid, 'team': team, 'season': season} for team, season in self.career]
        except:
            pass
        matches_data = [match.serialize(uid) for match in self.matches]
        return player_data, career_data, matches_data


def parse_base_info(name, base_info):
    date_of_birth, citizenship, height, weight = None, None, None, None
    try:
        date_of_birth_index = next(base_info.index(x) for x in base_info if x.text.strip('') == 'Дата рождения')
        date_of_birth = base_info[date_of_birth_index + 1].text.strip(' г.')  # ' 27.11.1982 г. ' to '27.11.1982'
    except:
        pass
    try:
        citizenship_index = next(base_info.index(x) for x in base_info if x.text.strip('') == 'Гражданство')
        citizenship = base_info[citizenship_index + 1].text.strip()  # ' Россия' to 'Россия'
    except:
        pass
    try:
        weight_index = next(base_info.index(x) for x in base_info if x.text.strip('') == 'Вес')
        weight = base_info[weight_index + 1].text.strip(' кг')  # ' 74 кг' to '74'
    except:
        pass
    try:
        height_index = next(base_info.index(x) for x in base_info if x.text.strip('') == 'Рост')
        height = base_info[height_index + 1].text.strip(' см.')  # ' 176 см.' to '174'
    except:
        pass
    return Player(name, date_of_birth, citizenship, height, weight)


def parse_career(career_info):
    career = []
    if len(career_info) < 2:
        seasons = career_info[0].find_all("tr")
    else:
        seasons = career_info[1].find_all("tr", recursive=False)

    for season in seasons:
        try:
            club_name = season.find_all('a')[1].text.strip()
            club_season = season.find("td", {"class": "zayavka blue"}).text.strip()
            career.append((club_name, club_season))
        except:
            pass
    return career


def get_season_map(season_info):
    season_map = {}
    for season in season_info:
        season_id = season.get('rel')
        season_year = season.find("div", {"class": "year"}).text.strip()
        season_map[season_id] = season_year
    return season_map


def parse_season(season_year, season):
    player_matches = []
    matches = season.find_all("tr", {"class": "good"})
    for match_info in matches[1:]:
        tournament = match_info.find("td", {"class": "tournament"}).text.strip()
        date = match_info.find("td", {"class": "date"}).text.strip()
        match = match_info.find("td", {"class": "match"}).text.strip()
        result = match_info.find("td", {"class": "result"}).text.strip()
        minutes = match_info.find("td", {"class": "minutes"}).text.strip()
        goals = match_info.find("td", {"class": "other blue goal"}).text.strip()
        scored_penalties = match_info.find("td", {"class": "other blue pen_ok"}).text.strip()
        unscored_penalties = match_info.find("td", {"class": "other blue pen_no"}).text.strip()
        yellow_card = match_info.find("td", {"class": "other blue yc"}).text.strip()
        yellow_red_card = match_info.find("td", {"class": "other blue yrc"}).text.strip()
        red_card = match_info.find("td", {"class": "other blue rc"}).text.strip()
        player_match = Match(season_year, tournament, date, match, result, minutes, goals, scored_penalties,
                             unscored_penalties, yellow_card, yellow_red_card, red_card)
        player_matches.append(player_match)
    return player_matches




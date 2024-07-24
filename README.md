# Russian Football Data

The dataset includes information about all football matches (RFPL, RPL, Russian Cup) and all players being in a team sheets in a period between from 2002 to 2024.

## Data Description

### players
- uid - unique player's ID (primary keyl unique field)
- name - name of the player
- date_of_birth - date of birth
- citizenship - citizenship
- height - height (cm)
- weight - weight (kg)

<img src="https://github.com/g2r4i6e8/russian_football_data/blob/main/docs/players.png" height="400" />

### matches
- uid - player's uid (that is not unique field)
- season - years of the season (e.g. 2012/2013)
- tournament - name of the tournament (КР - Кубок России, ТД - Турнир дублёров (до 2008) / МП - Молодёжное первенство (с 2008), ЧР - Чемпионат России (до 2018) / РПЛ - Российская премьер лига (с 2018), СКР - Суперкубок России, ПТ - ?)
- date - date of the match
- match - teams
- result - the final result
- minutes - the range of minutes the player was on the pitch
- goals - number of goals scored by the player
- scored_penalties - number of penalties scored by the player
- unscored_penalties - number of penalties not scored by the player
- yellow_card - one yellow card obtained by the player
- yellow_red_card - two yellow cards (-> red card) obtained by the player
- red_card - direct red card obtained by the player

<img src="https://github.com/g2r4i6e8/russian_football_data/blob/main/docs/matches.png" height="400" />

### careers
- uid - player's uid (that is not unique field)
- team - name of the team
- season - years of the season (e.g. 2012/2013)

NB! One player can play in two teams during one season

<img src="https://github.com/g2r4i6e8/russian_football_data/blob/main/docs/careers.png" height="400" />

## Getting Started
 
```
import pandas as pd
careers = pd.read_csv('careers.csv.gz')
players = pd.read_csv('players.csv.gz')
matches = pd.read_csv('matches.csv.gz')
```


## Data Source
[Russian Premier Ligue Official Website](https://premierliga.ru/)

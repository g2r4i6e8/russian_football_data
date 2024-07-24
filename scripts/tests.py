from scripts.run import collect_player_data

def test_player_info_collection():
    player_urls = ['/players/Kokorin-Aleksandr', '/players/Aitov-Tagir', '/players/Ayssaui-Sid-Ahmed']
    players, errors = collect_player_data(player_urls, False)
    player1 = players[0]
    assert player1.name == ('Кокорин Александр Александрович')
    assert len(player1.career) == 16
    assert len(player1.matches) == 303
    assert sum([int(x.goals) for x in player1.matches if x.season=="2011/2012"]) == 12
    player2 = players[1]
    assert player2.name == ('Аитов Тагир Минсагитович')
    assert player2.citizenship == 'Россия'
    player3 = players[2]
    assert player3.name == ('Айссауи Сид Ахмед')

    return True

if __name__ == "__main__":
    test_player_info_collection()

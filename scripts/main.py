import os.path
import pickle

from scripts.run import collect_player_urls, collect_player_data, serialize_data

if __name__ == "__main__":

    if not os.path.exists(os.path.join(os.pardir, 'raw_data', 'player_urls.pickle')):
        collect_player_urls()
    with open(os.path.join(os.pardir, 'raw_data', 'player_urls.pickle'), 'rb') as handle:
        player_urls = pickle.load(handle)
    collect_player_data(player_urls)
    serialize_data()

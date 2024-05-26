import requests
import json
import Coins
import sys
import time
import threading
from functools import wraps
import CoinDB


def load_search(data):
    search_key = ""
    for i in data:
        search_key = search_key + i.ADRESS + ','
    return search_key
def show_loading_decorator(message):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            stop_event = threading.Event()
            loading_thread = threading.Thread(target=show_loading, args=(message, stop_event))
            loading_thread.start()
            try:
                result = func(*args, **kwargs)
            finally:
                stop_event.set()
                loading_thread.join()
                print(f"\r{message} Successful!   ")
            return result
        return wrapper
    return decorator

# Function to show loading indicator
def show_loading(message, stop_event):
    while not stop_event.is_set():
        for char in ['.  ', '.. ', '...']:
            sys.stdout.write(f'\r{message}{char}')
            sys.stdout.flush()
            if stop_event.wait(0.5):
                break
@show_loading_decorator("Get Coins from Base DataBase: ")
def get_baseCoins():
    coins = []
    coin_list = CoinDB.get_all_basecoins()
    for item in coin_list:
        coin = Coins.Coin(item["coin_name"], item['coin_sym'], item['coin_address'], item['blockchain'], item['volume'], item['market_cap'], item['added_date'])
        coins.append(coin)
    return coins
@show_loading_decorator("Get pairs from DEX: ")
def getpairs(coins):
    Data = []
    chunck_size = 29
    for i in range(0,len(coins), chunck_size):
        chunk = coins[i:i+chunck_size]
        search_key = load_search(chunk)
        url = "https://api.dexscreener.com/latest/dex/tokens/{}".format(search_key)
        my_request = requests.get(url)
        print(my_request)
        infos = json.loads(my_request.text)
        if isinstance(infos['pairs'], list):
           for info in infos['pairs']:
            if info['quoteToken']['name'] == 'Wrapped Ether':
                    Data.append(info)
        
    return Data

@show_loading_decorator("Creating COININFO objects: ")
def create_CoinInfo(datas):
    coinsinfos = []
    for data in datas:
        coininfo = Coins.CoinInfo(data)
        coinsinfos.append(coininfo)
    return coinsinfos
@show_loading_decorator("Save Coins Info to DataBase: ")
def save_to_database(coinsinfos):
    for coininfo in coinsinfos:
        CoinDB.add_coin_info_to_db(coininfo)
    
def main():
    coins = get_baseCoins()
    datas = getpairs(coins)
    coinsinfos = create_CoinInfo(datas)
    save_to_database(coinsinfos)
    
if __name__ == "__main__":
    main()
        
import requests
import re
from bs4 import BeautifulSoup
import Coins
from datetime import datetime, timedelta
import CMCrequest
import sys
import time
import threading
from functools import wraps

def Check_ETH(Coin):
    if Coin.BC == "Ethereum":
        return True
    else:
        return False
def parse_relative_time(relative_time_str):
    # Get the current date and time
    now = datetime.now()
    
    # Parse the string to extract the number and the time unit (hours, days)
    match = re.match(r'(\d+)\s+(minutes?|hours?|days?)\s+ago', relative_time_str)
    
    if not match:
        print(relative_time_str)
        raise ValueError("The input string is not in the correct format")
    
    number = int(match.group(1))
    unit = match.group(2)
    
    if 'minutes' in unit:
        delta = timedelta(minutes=number)
    elif 'hour' in unit:
        delta = timedelta(hours=number)
    elif 'day' in unit:
        delta = timedelta(days=number+1)
    
    # Calculate the past date
    past_date = now - delta
    
    # Return the date in "YYYY-MM-DD" format
    return past_date.strftime('%Y-%m-%d')
def extract_date(datetime_str):
    # Parse the datetime string to a datetime object
    datetime_obj = datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%S.%fZ')
    
    # Extract the date part
    date_obj = datetime_obj.date()
    
    return date_obj

def clean_number(input_string):
    # Use regex to remove the dollar sign and commas
    cleaned_string = re.sub(r'[$,]', '', input_string)
    return cleaned_string
def right_coin_info(coin,info):
    desired_name = coin.NAME
    desired_symbol = coin.SYM
    desired_date = coin.ADDT
    #print(desired_name," ",desired_symbol," ",desired_date)
    # Iterate over the list of dictionaries
    desired_info = []
    if len(info) == 1:
        return info[0]
    else:
        for item in info:
            if item['name'] == desired_name and item['symbol'] == desired_symbol:
                desired_info.append(item)
        if len(desired_info) == 1:
            #print(desired_info[0]['name'])
            return desired_info[0]
        else: 
            for item in desired_info: 
                check_date = extract_date(item['date_added'])
                date_obj = datetime.strptime(desired_date, '%Y-%m-%d').date()
                desired_datep = date_obj + timedelta(days=1)
                desired_datem = date_obj - timedelta(days=1)
                if str(check_date) == str(desired_date):
                    return item
                if str(check_date) == str(desired_datep):
                    return item
                if str(check_date) == str(desired_datem):
                    return item
            


def Get_Adress(ETH_coins,info):
    for coin in ETH_coins:
        #print(info[coin.SYM])
        #print("new")
        d = right_coin_info(coin,info[coin.SYM])
        coin.ADRESS = d['contract_address'][0]['contract_address']
    
def has_no_spaces(input_string):
    # Check if there is a space in the string
    if ' ' in input_string:
        return False
    else:
        if '!' in input_string:
            return False
        else:
            return True

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

@show_loading_decorator("Bulid ETH coins Symbol List:")
def build_syms(ETH_c):
    ETH_Syms = []
    for coin in ETH_c:
       ETH_Syms.append(coin.SYM) 
    return ETH_Syms

@show_loading_decorator("Get the info from CMC API:")
def Getinfo(Syms):
    datas = CMCrequest.MetadataV2(Syms)
    info = datas['data']
    return info        

@show_loading_decorator("Get New Coins from CMC site:")
def GettingNewCoins():
    ETH_Coin_count = 0

    my_request = requests.get("https://coinmarketcap.com/new/")


    print(" HTML request: ",my_request)

    soup = BeautifulSoup(my_request.text, "html.parser")

    names = soup.find_all("p", attrs={"class":"sc-4984dd93-0 kKpPOn"}) 
    syms = soup.find_all("p", attrs={"class":"sc-4984dd93-0 iqdbQL coin-item-symbol"})

    #soup.find_all("div",attrs={"class":"sc-bd8d8238-3 cTyzfx"})

    Everything = soup.find_all("td")
    BlockChains = [] 
    Names = []
    Syms = []
    Vols = []
    MarketCap = []
    Times = []

    coins = []
    i = 0
    for item in Everything:
        if i == 8:
            BlockChains.append(item.text)
        if i == 7:
            Vols.append(clean_number(item.text))
        if i == 6: 
            MarketCap.append(clean_number(item.text))
        if i == 9:
            Times.append(parse_relative_time(item.text))
        i += 1
        if i == 10:
            i = 0
    for name in names: 
        Names.append(name.text)
    for sym in syms:
        Syms.append(sym.text)

    for n in range(len(Names)):
        coin = Coins.Coin(Names[n],Syms[n],None,BlockChains[n],Vols[n],MarketCap[n],Times[n])
        coins.append(coin)
    ETH_Coins = []
    right_coins = []
    for c in coins:
            if has_no_spaces(c.SYM):
                right_coins.append(c)
    for coin in right_coins:
        if Check_ETH(coin):
            ETH_Coins.append(coin)
    ETH_Coin_count = len(ETH_Coins)


    page = 2
    while page <= 4:
        BlockChains = [] 
        Names = []
        Syms = []
        Vols = []
        MarketCap = []
        Times = []

        url = "https://coinmarketcap.com/new/?page={}".format(str(page))
        my_request2 = requests.get(url)
        print(" HTML request: ",my_request2)
        soup2 = BeautifulSoup(my_request2.text, "html.parser")
        names = soup2.find_all("p", attrs={"class":"sc-4984dd93-0 kKpPOn"}) 
        syms = soup2.find_all("p", attrs={"class":"sc-4984dd93-0 iqdbQL coin-item-symbol"})
        Everything = soup2.find_all("td")
        i = 0
        for item in Everything:
            if i == 8:
                BlockChains.append(item.text)
            if i == 7:
                Vols.append(clean_number(item.text))
            if i == 6: 
                MarketCap.append(clean_number(item.text))
            if i == 9:
                Times.append(parse_relative_time(item.text))
            i += 1
            if i == 10:
                i = 0

        for name in names: 
            Names.append(name.text)
        for sym in syms:
            Syms.append(sym.text)
        
        page += 1
        coins = []
        for n in range(len(Names)):
            coin = Coins.Coin(Names[n],Syms[n],None,BlockChains[n],Vols[n],MarketCap[n],Times[n])
            coins.append(coin)
        right_coins = []
        for c in coins:
            if has_no_spaces(c.SYM):
                right_coins.append(c)
        for coin in right_coins:
            if Check_ETH(coin):
                ETH_Coins.append(coin)
        ETH_Coin_count = len(ETH_Coins)
    if ETH_Coin_count >= 100:    
        ETH_Coins = ETH_Coins[:99]
    ETH_Coin_count = len(ETH_Coins)
    print(" Number of ETH coins found: ",ETH_Coin_count)
    return ETH_Coins
@show_loading_decorator("Add to Database:")
def AddtoDB(ETH_Coins):
    for i in ETH_Coins:
        i.add_etherium_to_base()
def main():
    ETH_Coins = GettingNewCoins()
    ETH_Syms = build_syms(ETH_Coins)
    info = Getinfo(ETH_Syms)
    Get_Adress(ETH_Coins,info)
    AddtoDB(ETH_Coins)
if __name__ == "__main__":
    main()

    





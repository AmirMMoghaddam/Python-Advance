import requests
import re
from bs4 import BeautifulSoup
import Coins

my_request = requests.get("https://coinmarketcap.com/new/")
my_request2 = requests.get("https://coinmarketcap.com/new/?page=2")

print(my_request)
print(my_request2)

soup = BeautifulSoup(my_request.text, "html.parser")
soup2 = BeautifulSoup(my_request.text, "html.parser")
Names = []
#soup.find_all("p", attrs={"class":"sc-4984dd93-0 kKpPOn"}) 
#soup.find_all("p", attrs={"class":"sc-4984dd93-0 iqdbQL coin-item-symbol"})
BlockChains = [] 
#soup.find_all("div",attrs={"class":"sc-bd8d8238-3 cTyzfx"})

Everything = soup.find_all("td")
Everything2 = soup2.find_all("td")
Vols = []
MarketCap = []
Times = []

coins = []
i = 0
for item in Everything:    
    if i == 2:
        Names.append(item.text)
    if i == 8:
        BlockChains.append(item.text)
    if i == 7:
        Vols.append(item.text)
    if i == 6: 
        MarketCap.append(item.text)
    if i == 9:
        Times.append(item.text)
    i += 1
    if i == 10:
        i = 0
i = 0
for item in Everything2:    
    if i == 2:
        Names.append(item.text)
    if i == 8:
        BlockChains.append(item.text)
    if i == 7:
        Vols.append(item.text)
    if i == 6: 
        MarketCap.append(item.text)
    if i == 9:
        Times.append(item.text)
    i += 1
    if i == 10:
        i = 0
print(len(Names), " ",len(BlockChains), " ", len(Vols), " ",len(MarketCap), " ",len(Times), " ")

for n in range(len(Names)):
    coin = Coins.Coin(Names[n],None,None,BlockChains[n],Vols[n],Times[n])
    coins.append(coin)
for coin in coins:
    if coin.BC == "Ethereum" :
        coin.printCoin()
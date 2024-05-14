import re
import requests
from bs4 import BeautifulSoup

r = requests.get("https://divar.ir/s/karaj/car?q=h%2030%20%DA%A9%D8%B1%D8%A7%D8%B3")

print("The response was : " , r)

soup = BeautifulSoup(r.text ,"html.parser")

articles = soup.findAll("article", {"class": "kt-post-card kt-post-card--outlined kt-post-card--has-action"})
for article in articles: 
    name = article.find("h2")
    print(name.text)







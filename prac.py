import json
import requests
import time
from bs4 import BeautifulSoup as BS
import pandas as pd

def create_json(data):
    with open('data.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii='False')

def create_csv(data):
    dataframe = pd.DataFrame(data)
    dataframe.to_csv('data.csv', index=False, sep=';')

def search_list(data, key):
    items = []
    for item in data:
        if item.get("Name").upper().startswith(key.upper()):
            items.append(item)
    if not items:
        return "Not found"
    else:
        return items

HEADERS = {
    "Accept": "application/json, text/plain, */*",
    "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.141 YaBrowser/22.3.2.644 Yowser/2.5 Safari/537.36"
}
page = 1
crypto = []
for page in range(1,6):
    url = "https://coinmarketcap.com/?page=" + str(page)
    req = requests.get(url, headers=HEADERS)
    soup = BS(req.text,"lxml")
    blocks_tr = soup.find_all('tr')
    for item in blocks_tr:
        item_name = item.find_all('p', class_='sc-1eb5slv-0 iworPT')
        for name in item_name:
            item_Price = item.find_all('div', class_='sc-131di3y-0 cLgOOr')
            for price in item_Price:
                item_MarketCap = item.find_all('span', class_='sc-1ow4cwt-1 ieFnWP')
                for MarketCap in item_MarketCap:       
                    crypto.append(
                        {
                            'Name' : name.text,
                            'Price' : price.text,
                            'MarketCap' : MarketCap.text
                        }
                    )
    page +=1   
for item in crypto:
    print(item)
create_json(crypto)
create_csv(crypto)
while True:
    print("Please Enter Name Cryptocurrency: ")
    key = input()
    if (key == "0"): 
        quit()
    print(search_list(crypto, key))

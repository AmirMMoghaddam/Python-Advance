from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

def load_Meta(Syms):
    search_key = ''
    for i in Syms:
      search_key += i + ','
    return search_key[:-1]


def MetadataV2(Syms): 
  url = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/info'
  parameters = {
  'symbol': load_Meta(Syms)
  }
  headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': '16d2fbcf-d948-4d31-8020-9392a669d68b',
  }

  session = Session()
  session.headers.update(headers)

  try:
    response = session.get(url, params=parameters)
    data = json.loads(response.text)
    return data
  except (ConnectionError, Timeout, TooManyRedirects) as e:
    print(e)
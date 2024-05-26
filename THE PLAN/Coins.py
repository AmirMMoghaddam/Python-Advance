import CoinDB

class Coin:
    def __init__(self,NAME,SYM,ADRESS,BC,VOLUME,MC,ADDT):
        self.NAME = NAME
        self.SYM = SYM
        self.ADRESS = ADRESS
        self.BC = BC 
        self.VOLUME = VOLUME
        self.MC = MC
        self.ADDT = ADDT
    def printCoin(self):
        print("|Name| : ",self.NAME," |Symbol| : ",self.SYM," \n|Adress| : ",self.ADRESS," \n|Blockchains| : ",self.BC," |Volume| : ",self.VOLUME," |Added| : ",self.ADDT,"\n ---------")
    
    def add_etherium_to_base(self):
        CoinDB.add_to_base(self.NAME,self.SYM,self.ADRESS,self.BC,self.VOLUME,self.MC,self.ADDT)

class CoinInfo:
    def __init__(self, data):
        # General Information
        self.chainId = data.get('chainId')
        self.dexId = data.get('dexId')
        self.url = data.get('url')
        self.pairAddress = data.get('pairAddress')

        # Labels
        self.labels = data.get('labels')

        # Tokens
        base_token = data.get('baseToken', {})
        self.baseToken_address = base_token.get('address')
        self.baseToken_name = base_token.get('name')
        self.baseToken_symbol = base_token.get('symbol')

        quote_token = data.get('quoteToken', {})
        self.quoteToken_address = quote_token.get('address')
        self.quoteToken_name = quote_token.get('name')
        self.quoteToken_symbol = quote_token.get('symbol')

        # Prices
        self.priceNative = data.get('priceNative')
        self.priceUsd = data.get('priceUsd')

        # Transactions
        txns = data.get('txns', {})
        self.txns_m5 = txns.get('m5')
        self.txns_h1 = txns.get('h1')
        self.txns_h6 = txns.get('h6')
        self.txns_h24 = txns.get('h24')

        # Volume
        volume = data.get('volume', {})
        self.volume_m5 = volume.get('m5')
        self.volume_h1 = volume.get('h1')
        self.volume_h6 = volume.get('h6')
        self.volume_h24 = volume.get('h24')

        # Price Change
        price_change = data.get('priceChange', {})
        self.priceChange_m5 = price_change.get('m5')
        self.priceChange_h1 = price_change.get('h1')
        self.priceChange_h6 = price_change.get('h6')
        self.priceChange_h24 = price_change.get('h24')

        # Liquidity
        liquidity = data.get('liquidity', {})
        self.liquidity_usd = liquidity.get('usd')
        self.liquidity_base = liquidity.get('base')
        self.liquidity_quote = liquidity.get('quote')

        # Fully Diluted Valuation (FDV)
        self.fdv = data.get('fdv')

        # Creation Time
        self.pairCreatedAt = data.get('pairCreatedAt')

    def __str__(self):
        return (
            f"General Information:\n"
            f"  chainId: {self.chainId}\n"
            f"  dexId: {self.dexId}\n"
            f"  url: {self.url}\n"
            f"  pairAddress: {self.pairAddress}\n"
            f"Labels:\n"
            f"  labels: {self.labels}\n"
            f"Tokens:\n"
            f"  baseToken:\n"
            f"    address: {self.baseToken_address}\n"
            f"    name: {self.baseToken_name}\n"
            f"    symbol: {self.baseToken_symbol}\n"
            f"  quoteToken:\n"
            f"    address: {self.quoteToken_address}\n"
            f"    name: {self.quoteToken_name}\n"
            f"    symbol: {self.quoteToken_symbol}\n"
            f"Prices:\n"
            f"  priceNative: {self.priceNative}\n"
            f"  priceUsd: {self.priceUsd}\n"
            f"Transactions (buy/sell):\n"
            f"  m5: {self.txns_m5}\n"
            f"  h1: {self.txns_h1}\n"
            f"  h6: {self.txns_h6}\n"
            f"  h24: {self.txns_h24}\n"
            f"Volume:\n"
            f"  m5: {self.volume_m5}\n"
            f"  h1: {self.volume_h1}\n"
            f"  h6: {self.volume_h6}\n"
            f"  h24: {self.volume_h24}\n"
            f"Price Change (%):\n"
            f"  m5: {self.priceChange_m5}\n"
            f"  h1: {self.priceChange_h1}\n"
            f"  h6: {self.priceChange_h6}\n"
            f"  h24: {self.priceChange_h24}\n"
            f"Liquidity:\n"
            f"  usd: {self.liquidity_usd}\n"
            f"  base: {self.liquidity_base}\n"
            f"  quote: {self.liquidity_quote}\n"
            f"FDV:\n"
            f"  fdv: {self.fdv}\n"
            f"Creation Time:\n"
            f"  pairCreatedAt: {self.pairCreatedAt}\n"
        )
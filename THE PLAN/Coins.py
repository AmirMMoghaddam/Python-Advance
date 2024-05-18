

class Coin:
    def __init__(self,NAME,SYM,ADRESS,BC,VOLUME,ADDT):
        self.NAME = NAME
        self.SYM = SYM
        self.ADRESS = ADRESS
        self.BC = BC 
        self.VOLUME = VOLUME
        self.ADDT = ADDT
    def printCoin(self):
        print("|Name| : ",self.NAME," |Symbol| : ",self.SYM," |Adress| : ",self.ADRESS," |Blockchains| : ",self.BC," |Volume| : ",self.VOLUME," |Added| : ",self.ADDT)
    
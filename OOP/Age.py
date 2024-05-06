from datetime import date
import math
def GetbackDays(Month):
        i = 0
        while i < Month:
            if (i+1) % 2 == 1:
                yield 31
            else: 
                if (i+1) == 2:
                    yield 28
                else: 
                    yield 30
            i += 1
class Date:
    def __init__(self,Tarikh):
        self.Year = int(Tarikh[0])
        self.Month = int(Tarikh[1])
        self.Day = int(Tarikh[2])
    def Validation(self):
        if self.Month > 12:
            return False
        
        if self.Month % 2 == 1:
            if self.Day > 31 : 
                return False
        else:
            if self.Month == 2:
                if self.Day > 29 :
                    return False
            else:
                if self.Day > 30: 
                    return False
        return True
    def Month2day(self):
        sum = 0
        for i in GetbackDays(self.Month):
           sum += i
        return sum 
    def DaysFromStart(self):
        return (self.Year * 365) + self.Month2day() + self.Day
    def Distance(self , date2):
        Days1 = self.DaysFromStart()
        Days2 = date2.DaysFromStart()
        if Days1 > Days2: 
            return Days1 - Days2
        else: 
            return Days2 - Days1
        

today = date.today()
todayL = str(today).split("-")
TodayDate = Date(todayL)
BirthDay = input().split("/")
BirthDate = Date(BirthDay)
if BirthDate.Validation() :
    Dist = BirthDate.Distance(TodayDate)
    Age = math.floor(Dist/365)
    print(Age)
else: 
    print("WRONG")

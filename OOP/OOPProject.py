import random
import math
class Human:
    def __init__(self,Name):
        self.Name = Name
class Footballist(Human):
    def __init__(self,Name,Team):
        super().__init__(Name)
        self.Team = Team
    def PrintF(self):
        print(self.Name, " Team = ", self.Team )

Names = "حسین - مازیار - اکبر - نیما -  مهدی - فرهاد - محمد - خشایار - میلاد - مصطفی - امین - سعید - پویا - پوریا - رضا - علی - بهزاد - سهیل - بهروز - شهروز - سامان - محسن".split("-")



Acount = 0
Bcount = 0
for i in Names:
    if Acount < math.floor(len(Names) / 2) and Bcount < math.floor(len(Names) / 2):
        choises = ["A", "B"]
        team = random.choice(choises)
        if team == "A" :
             Acount += 1 
        else: 
           Bcount += 1
        Player = Footballist(i,team)
        Player.PrintF()
    else:
        if Acount >= math.floor(len(Names) / 2):
            Player = Footballist(i,"B")
            Player.PrintF()
            Bcount += 1 
        else:
            Player = Footballist(i,"A")
            Player.PrintF()
            Acount += 1
print(Acount," ",Bcount)
        

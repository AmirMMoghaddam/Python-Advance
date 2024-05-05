class Student:
    def __init__(self,Age,Height,Weight):
        self.Age = Age
        self.Weight = Weight
        self.Height = Height
    
class School: 
    def __init__(self,Name,Number,Ages,Heights,Weights):
        self.Name = Name
        self.Number= Number
        self.Students = []
        for i in range(self.Number):
            self.Students.append(Student(Ages[i],Heights[i],Weights[i]))
    def Average(self): 
        sumAge = 0
        sumHeights = 0
        sumWeight = 0 
        for item in self.Students:
            sumAge += item.Age
            sumHeights += item.Height
            sumWeight += item.Weight
        return [sumAge/self.Number ,sumHeights/self.Number, sumWeight/self.Number]
ANumbers = int(input())

AAges = list(map(lambda x: int(x),input().split()))
AHeights = list(map(lambda x: int(x),input().split()))
AWeights = list(map(lambda x: int(x),input().split()))

SchoolA = School("A",ANumbers,AAges,AHeights,AWeights)

BNumbers = int(input())

BAges = list(map(lambda x: int(x),input().split()))
BHeights = list(map(lambda x: int(x),input().split()))
BWeights = list(map(lambda x: int(x),input().split()))

SchoolB = School("B",BNumbers,BAges,BHeights,BWeights)

Avereges = [SchoolA.Average() , SchoolB.Average()]
for item in Avereges: 
   for i in item:
       print(i)
if Avereges[0][1] > Avereges[1][1]:
    print("A")
if Avereges[0][1] < Avereges[1][1]:
    print("B")
if Avereges[0][1] == Avereges[1][1]:
    if Avereges[0][2] > Avereges[1][2]:
        print("A")
    if Avereges[0][2] < Avereges[1][2]:
        print("B")
    if Avereges[0][2] == Avereges[1][2]:
        print("Same")
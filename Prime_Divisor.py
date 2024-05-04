
def Prime_Divisor(number):
    Divisor =[]
    Divisor.append(1)
    for p in range(number):
        if number % (p+2) == 0: 
            if Is_Prime(p+2):
                Divisor.append(p+2)
    return Divisor
def All_Divisor(number):
    Divisor =[]
    Divisor.append(1)
    for p in range(number):
        if number % (p+2) == 0: 
           Divisor.append(p+2)
    return Divisor


def Is_Prime(number):
    if number < 0:
        number = -1*number
    if number < 1:
        return False
    if number == 1:
        return True
    if number > 1:
        Divisor = All_Divisor(number)
        if len(Divisor) == 2:
            return True
        else:
            return False

Inputs = []
for i in range(10):
    Inputs.append(int(input("Enter a Number : ")))
Divisor = []
Output = 0
for number in Inputs: 
    tempDivisor = Prime_Divisor(number)
    if len(tempDivisor) >= len(Divisor):
        if number > Output:
            Output = number
            Divisor = tempDivisor
print(Output,len(Divisor)-1)
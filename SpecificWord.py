paragraph = input()
Allwords = paragraph.split()

for i in range(len(Allwords)):
    if i != 0:
        if Allwords[i][0].isupper():
            if Allwords[i-1][len(Allwords[i-1])-1] != "." and  Allwords[i-1][len(Allwords[i-1])-1] != "," :
                l = list(Allwords[i])
                l.remove(".") if "." in l else None
                l.remove(",") if "," in l else None
                word = "".join(l)
                print(i+1,":",word)
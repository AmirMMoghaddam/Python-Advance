Genre = {"Horror": 0, "Romance" : 0, "Comedy" : 0, "History": 0 , "Adventure": 0 , "Action": 0}
GenreList =[]
for Key in Genre:
    GenreList.append(Key)
input_count = int(input())

#Getting the inputs
for i in range(input_count):
    Input = input().split()
    for j in range(3):
        Genre[Input[j+1]] += 1
#Sort Genres
SortedGenreList = []

while len(GenreList) != 0:
    tempGenre =""
    maxpoints = 0
    for genre in GenreList:
        if  Genre[genre] > maxpoints:
            maxpoints =  Genre[genre]
            tempGenre = genre
        if Genre[genre] == maxpoints:
            if maxpoints == 0:
                tempGenre = genre
            else:
                tempGenre = sorted([genre,tempGenre])[0]
    SortedGenreList.append(tempGenre)
    GenreList.remove(tempGenre)
#Print 
for genre in SortedGenreList: 
    print(genre," : ",Genre[genre])
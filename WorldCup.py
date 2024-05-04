
GroupB = {"Iran": {"wins" : 0,"loses" : 0, "draws":0, "goal difference": 0, "points": 0},"Spain" : {"wins" : 0,"loses" : 0, "draws":0, "goal difference": 0, "points": 0}, "Portugal" : {"wins" : 0,"loses" : 0, "draws":0, "goal difference": 0, "points": 0},"Morocco": {"wins" : 0,"loses" : 0, "draws":0, "goal difference": 0, "points": 0}}
Games = [["Iran","Spain"],["Iran","Portugal"],["Iran","Morocco"],["Spain","Portugal"],["Spain","Morocco"],["Portugal","Morocco"]]
Teams =[]
for Key in GroupB:
    Teams.append(Key)

# Getting Inputs
for i in range(len(Games)):
    Input = input()
    Team1Goals = int(Input[0])
    Team2Goals = int(Input[2])
    if Team1Goals > Team2Goals: 
        GroupB[Games[i][0]]["wins"] += 1
        GroupB[Games[i][1]]["loses"] += 1
        GroupB[Games[i][0]]["points"] += 3
    if Team1Goals < Team2Goals: 
        GroupB[Games[i][1]]["wins"] += 1
        GroupB[Games[i][0]]["loses"] += 1
        GroupB[Games[i][1]]["points"] += 3
    if Team1Goals == Team2Goals: 
        GroupB[Games[i][0]]["draws"] += 1
        GroupB[Games[i][1]]["draws"] += 1
        GroupB[Games[i][0]]["points"] += 1
        GroupB[Games[i][1]]["points"] += 1
    GroupB[Games[i][0]]["goal difference"] += Team1Goals - Team2Goals
    GroupB[Games[i][1]]["goal difference"] += Team2Goals - Team1Goals
#Sorting the teams
SortedTeams = [] 

while len(Teams) != 0:
    tempteam =""
    maxpoints = 0
    for team in Teams:
        if  GroupB[team]["points"] > maxpoints:
            maxpoints = GroupB[team]["points"]
            tempteam = team
        if GroupB[team]["points"] == maxpoints:
            if maxpoints == 0:
                tempteam = team
            else:
                if GroupB[team]["wins"] > GroupB[tempteam]["wins"]:
                    tempteam = team
                if GroupB[team]["wins"] == GroupB[tempteam]["wins"]:
                    tempteam = sorted([team,tempteam])[0]
    SortedTeams.append(tempteam)
    Teams.remove(tempteam)

#Print Output
for team in SortedTeams:
    print(team," wins : ",GroupB[team]["wins"]," , loses : ",GroupB[team]["loses"]," , draws : ",GroupB[team]["draws"]," , goal difference : ",GroupB[team]["goal difference"]," , points : ",GroupB[team]["points"])
     


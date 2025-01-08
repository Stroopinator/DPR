import statbotics 
import csv
import pandas as pd
from IPython.display import display
from tabulate import tabulate


class team:
    name = ""
    number = 0
    dRating = 1
    games = 1
    matchDPR = []

    def __init__(self, name, number):
        self.name = name
        self.number = number
        self.dRating = 0
        self.games = 0

    def getDPR(self):
        if self.games == 0:
            return "Invalid"
        return str(round(self.dRating/self.games,2))

    def make_team(self, name, number):
        _team = team(name, number)
        return _team
    
    def formatData(self):
        return str(str(self.number) + " " + self.name + " " + str(self.getDPR())) 
    
    def addMatch(self, EPR, APR):
        if isinstance(EPR, (int, float)) & isinstance(APR, (int, float)):
            #print(str(self.dRating) + " " + str(self.games))
            self.dRating += EPR - APR
            self.games += 1
            self.matchDPR.append(EPR - APR)
        else:
            self.matchDPR.append("Invalid")

    def getName(self):
        return self.name
    
    def getNumber(self):
        return self.number

    

def getColor(team, match):
    if team == match["red_1"] | team == match["red_2"] | team == match["red_3"]:
        return True
    return False

def inMatch(team, match):
    return team == match["red_1"] | team == match["red_2"] | team == match["red_3"] | team == match["blue_1"] | team == match["blue_2"] | team == match["blue_3"]

sb = statbotics.Statbotics()
_event = "2024wasam"
teams = sb.get_teams(district = 'pnw', active = True)
dict = {}
tempDict = {'Number' : [],
        'Name' : [],
        'DPR': []} 
dataOut = []



#print(sb.get_team_events(team = 5827, year = 2024))

for t in teams:
    cur = team(sb.get_team(t["team"])["name"], t["team"])
    for i in sb.get_matches(team = cur.getNumber(), year = 2024):
        if(i["comp_level"] != "qm"):
            if getColor(cur.getNumber(), i):
                cur.addMatch(i["blue_teleop_epa_sum"], i["blue_teleop"])
            else: 
                cur.addMatch(i["red_teleop_epa_sum"], i["red_teleop"])
    tempDict['Number'].append(cur.getNumber())
    tempDict['Name'].append(cur.getName())
    tempDict['DPR'].append(cur.getDPR())
    dict[cur.getNumber()] = cur


#for i in dict:
    #print(dict[i].getName() + " " + dict[i].getDPR())
    #print(dict[i].formatData())
    #dataOut.append([dict[i].formatData()])

df = pd.DataFrame(tempDict)
print(tabulate(df, headers = 'keys', tablefmt = 'psql'))
#df.style
#df.to_csv('dataFile.csv', index=False)
df.to_excel('DataFrame.xlsx', sheet_name='Sheet1', index=False)
#display(df)

#with open('dataFile.csv', mode='w', newline='') as file:
    #writer = csv.writer(file)
    #for i in dataOut:
        #writer.writerows([i])

print("all done fuck off")







import statbotics 
import csv
import pandas as pd
from IPython.display import display
from tabulate import tabulate
import numpy as np


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

def getMatchDPR(match, color):
    if color:
        return match["blue_teleop_epa_sum"] - match["blue_teleop"]
    return  match["red_teleop_epa_sum"] - match["red_teleop"]



sb = statbotics.Statbotics()
temp = 0
_event = "2024wasam"
teams = sb.get_team_events(event = '2024wasno')
matches = sb.get_matches(event = '2024wasno')

dict = {}
teamDict = {}
tempDict = {'Number' : [],
        'Name' : [],
        'DPR': []}
dataOut = []


matchArray = np.zeros((len(matches)*2, len(teams)))
matchDPRArray = np.zeros(len(matches)*2)

tempTeamNum = 0
for t in teams:
    teamDict[t["team"]] = tempTeamNum
    tempTeamNum += 1







#print(sb.get_team_events(team = 5827, year = 2024))
matchCount = 0
for m in matches:
    matchArray[matchCount][teamDict[m["red_1"]]] = 1
    matchArray[matchCount][teamDict[m["red_2"]]] = 1
    matchArray[matchCount][teamDict[m["red_3"]]] = 1
    matchDPRArray[matchCount] = getMatchDPR(m, True)

    matchCount += 1

    matchArray[matchCount][teamDict[m["blue_1"]]] = 1
    matchArray[matchCount][teamDict[m["blue_2"]]] = 1
    matchArray[matchCount][teamDict[m["blue_3"]]] = 1
    matchDPRArray[matchCount] = getMatchDPR(m, False)

    matchCount += 1

#DO NOT TOCUH PLEASE
    
#print(matchArray)
#print(matchDPRArray)
dprs = np.linalg.lstsq(matchArray, matchDPRArray)   

#matchNorm = np.dot(np.transpose(matchArray), matchArray)
#DPRNorm = np.dot(np.transpose(matchArray), matchDPRArray)

for t in teams:
    print(str(t["team"]) + " " + str(dprs[0][teamDict[t["team"]]]))


    
#print(np.linalg.solve(matchNorm, DPRNorm))


#for i in dict:
    #print(dict[i].getName() + " " + dict[i].getDPR())
    #print(dict[i].formatData())
    #dataOut.append([dict[i].formatData()])

df = pd.DataFrame(tempDict)
pd.set_option('display.max_rows', None)
print(tabulate(df, headers = 'keys', tablefmt = 'psql'))
#df.style
#df.to_csv('dataFile.csv', index=False)
#df.to_excel('DataFrame.xlsx', sheet_name='Sheet1', index=False)
#display(df)

#with open('dataFile.csv', mode='w', newline='') as file:
    #writer = csv.writer(file)
    #for i in dataOut:
        #writer.writerows([i])

print("all done fuck off")







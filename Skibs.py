import statbotics 
import csv
import pandas as pd
from IPython.display import display
from tabulate import tabulate
import numpy as np
import sys


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
_event = "2024pncmp"
teams = sb.get_team_events(event = _event)
matches = sb.get_matches(event = _event)

dict = {}
teamDict = {}
tempDict = {'Number' : [],
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
    #if m["comp_level"] == "qm":
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

floor = sys.maxsize
ceiling = -sys.maxsize - 1
for dpr in dprs[0]:
    ceiling = max(ceiling, dpr)
    floor = min(floor, dpr)




#matchNorm = np.dot(np.transpose(matchArray), matchArray)
#DPRNorm = np.dot(np.transpose(matchArray), matchDPRArray)

for t in teams:
    tempDict["Number"].append(t["team"])
    tempDict["DPR"].append(round((dprs[0][teamDict[t["team"]]] + abs(floor)) / (abs(floor) + ceiling),2))


    
#print(np.linalg.solve(matchNorm, DPRNorm))


print(dprs[1])
df = pd.DataFrame(tempDict)
sorted_df = df.sort_values(by='DPR', ascending=False)
pd.set_option('display.max_rows', None)
print(tabulate(sorted_df, headers = 'keys', tablefmt = 'psql'))








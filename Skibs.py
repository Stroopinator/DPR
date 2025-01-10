import statbotics 
import csv
import pandas as pd
from IPython.display import display
from tabulate import tabulate
import numpy as np
import sys


class team:
    _matchDPR = []
    _number = 0
    _totalDPR = 0

    def __init__(self, number):
         _number = number

    def getNumber(self):
         return self._number         
    
    def addMatch(self, DPR):
         self._matchDPR.append(DPR)
         self._totalDPR += DPR

    def getSDV(self):
        mean = self._totalDPR/len(self._matchDPR)
        ans = 0
        for dpr in self._matchDPR:
            ans += pow(mean - dpr,2)

        ans = ans/len(self._matchDPR)
        return ans ** 0.5
         

def getMatchDPR(match, color):
    if color:
        return match["blue_teleop_epa_sum"] - match["blue_teleop"]
    return  match["red_teleop_epa_sum"] - match["red_teleop"]



sb = statbotics.Statbotics()
_event = "2024cmptx"
teams = sb.get_team_events(event = _event)
matches = sb.get_matches(event = _event)

teamDict = {}
tempDict = {'Number' : [],
        'DPR': [],
        'SDV' : []}
SDVDict = {}
dataOut = []


matchArray = np.zeros((len(matches)*2, len(teams)))
matchDPRArray = np.zeros(len(matches)*2)

tempTeamNum = 0
for t in teams:
    cur = team(t["team"])
    SDVDict[t["team"]] = cur
    teamDict[t["team"]] = tempTeamNum
    tempTeamNum += 1







#print(sb.get_team_events(team = 5827, year = 2024))
matchCount = 0
for m in matches:
    #if m["comp_level"] == "qm":
        matchArray[matchCount][teamDict[m["red_1"]]] = 1
        matchArray[matchCount][teamDict[m["red_2"]]] = 1
        matchArray[matchCount][teamDict[m["red_3"]]] = 1
        SDVDict[m["red_1"]].addMatch(getMatchDPR(m, True))
        SDVDict[m["red_2"]].addMatch(getMatchDPR(m, True))
        SDVDict[m["red_3"]].addMatch(getMatchDPR(m, True))
        matchDPRArray[matchCount] = getMatchDPR(m, True)

        matchCount += 1

        matchArray[matchCount][teamDict[m["blue_1"]]] = 1
        matchArray[matchCount][teamDict[m["blue_2"]]] = 1
        matchArray[matchCount][teamDict[m["blue_3"]]] = 1
        SDVDict[m["blue_1"]].addMatch(getMatchDPR(m, False))
        SDVDict[m["blue_2"]].addMatch(getMatchDPR(m, False))
        SDVDict[m["blue_3"]].addMatch(getMatchDPR(m, False))
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
    #dataOut({t["team"], dprs[0][teamDict[t["team"]]]})
    tempDict["Number"].append(t["team"])
    tempDict["DPR"].append(round((dprs[0][teamDict[t["team"]]] + abs(floor)) / (abs(floor) + ceiling),2))
    tempDict["SDV"].append(SDVDict[t["team"]].getSDV())


    
#print(np.linalg.solve(matchNorm, DPRNorm))


print(dprs[1])
df = pd.DataFrame(tempDict)
sorted_df = df.sort_values(by='DPR', ascending=False)
pd.set_option('display.max_rows', None)
df.to_excel('DataFrame.xlsx', index=False)
print(tabulate(sorted_df, headers = 'keys', tablefmt = 'psql'))








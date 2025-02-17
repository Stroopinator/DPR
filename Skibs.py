import statbotics 
import csv
import pandas as pd
from openpyxl import load_workbook
from IPython.display import display
from tabulate import tabulate
import numpy as np
import sys


class team:
    def __init__(self, number):
        self._matchDPR = []
        self._number = number
        self._totalDPR = 0

    def getNumber(self):
        return self._number         
    
    def addMatch(self, DPR):
        self._matchDPR.append(DPR) 
        self._totalDPR += DPR

    def getSDV(self):
        return round(np.std(a = self._matchDPR, ddof = 1),2)
         

def getMatchDPR(match, color):

    sum = 0
    #TODO: make sure games that dont exist are added
    if color:
        for t in match['alliances']['blue']['team_keys']:
            sum += teams[t]['epa']['breakdown']['teleop_points'] 
        return sum - match['result']["blue_teleop_points"]
    else:
        for t in match['alliances']['red']['team_keys']:
            sum += teams[t]['epa']['breakdown']['teleop_points'] 
        return sum - match['result']["red_teleop_points"]





file_path = 'Stats/DataFrame.xlsx'
workBook = load_workbook(file_path)

# Delete all sheets
for sheet_name in workBook.sheetnames:
    del workBook[sheet_name]

# Save the workbook
sb = statbotics.Statbotics()



while(True):
    _event = input("Enter Comp: ")
    if _event == "quit": break
    print(_event)

    #this query is currently broken and cannot be used
    #for now I will get a list of teams from the matches
    #TODO: uncomment this when it is fixed
    #teams = sb.get_team_events(event = _event)

    #matches = sb.get_matches(event = _event)
    matches = sb.get_matches(event = _event, limit = 1000)
    Tempteams = sb.get_team_events(event = _event, limit = 1000)
    teams = {}

    for t in Tempteams:
        teams[t['team']] = t
  

    teamDict = {}
    tempDict = {'Number': [],
            'DPR': [],
            'EPA' : [],
            'SDV' : []}
    SDVDict = {}
    dataOut = []


    matchArray = np.zeros((len(matches)*2, len(teams)))
    matchDPRArray = np.zeros(len(matches)*2)

    tempTeamNum = 0

    #this is changed from t["team"] to just t for the workaround
    #TODO: change this back when the API gets fixed
    for t in Tempteams:
        cur = team(t['team'])
        SDVDict[t['team']] = cur
        teamDict[t['team']] = tempTeamNum
        tempTeamNum += 1







    #print(sb.get_team_events(team = 5827, year = 2024))
        #could have broken something here
    matchCount = 0
    for m in matches:
        if m['result']['red_teleop_points'] != None and m['result']['blue_teleop_points'] != None:
            redDPR = getMatchDPR(m,True)

            for t in m['alliances']['red']['team_keys']:
                matchArray[matchCount][teamDict[t]] = 1
                SDVDict[t].addMatch(getMatchDPR(m, True))

            matchDPRArray[matchCount] = getMatchDPR(m, True)
            matchCount += 1

            blueDPR = getMatchDPR(m,False)

            for t in m['alliances']['blue']['team_keys']:
                matchArray[matchCount][teamDict[t]] = 1
                SDVDict[t].addMatch(getMatchDPR(m, False))

                #not sure whether this line goes in the loop or not
            matchDPRArray[matchCount] = getMatchDPR(m, False)
            matchCount += 1

    #DO NOT TOCUH PLEASE
        
    #print(matchArray)
    #print(matchDPRArray)
    dprs = np.linalg.lstsq(matchArray, matchDPRArray, rcond=None)   

    floor = sys.maxsize
    ceiling = -sys.maxsize - 1
    for dpr in dprs[0]:
        ceiling = max(ceiling, dpr)
        floor = min(floor, dpr)




    #matchNorm = np.dot(np.transpose(matchArray), matchArray)
    #DPRNorm = np.dot(np.transpose(matchArray), matchDPRArray)
        
    #like all other changes this was made to workaround get_teams_events being broken chagne back when it is fixed
    #TODO: fix this later
    for t in teams:
        #dataOut({t["team"], dprs[0][teamDict[t["team"]]]})
        tempDict['EPA'].append(teams[t]['epa']['breakdown']['total_points'])
        tempDict["Number"].append(t)
        tempDict["DPR"].append(round((dprs[0][teamDict[t]] + abs(floor)) / (abs(floor) + ceiling),2))
        tempDict["SDV"].append(SDVDict[t].getSDV())
        #tempDict["Name"].append(name_dict[t["team"]])
        


        
    #print(np.linalg.solve(matchNorm, DPRNorm))


    print(dprs[1])
    df = pd.DataFrame(tempDict)
    sorted_df = df.sort_values(by='DPR', ascending=False)
    pd.set_option('display.max_rows', None)
    print(tabulate(sorted_df, headers = 'keys', tablefmt = 'psql', showindex=False))

    new_sheet = workBook.create_sheet(title=_event)
    workBook.save(file_path)

    df.to_excel(file_path, index=False, sheet_name=_event)
    print(workBook.sheetnames)





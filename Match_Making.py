import pandas as pd
import random
import gspread
from datetime import date

'''Getting the Data from Google Sheets'''
def get_data():
    gc = gspread.service_account(filename='service_account.json')
    # Open a sheet from a spreadsheet in one go
    wks = gc.open('Main').sheet1
    df = pd.DataFrame(wks.get_all_records())
    team_id = df["Team Number"]
    score = df["Total Score"]
    teams_played = df["Teams Played"]
    teams_played = teams_played.astype(str)
    for i in range(len(teams_played)):
        teams_played[i] = teams_played[i].split(",")
    team_id = list(team_id)
    score = list(score)
    teams_played = list(teams_played)
    return team_id, score, teams_played

'''Match Making System'''
def match_making(team_id, points, team_played):
    #team_id: a list of teams
    #points: a list of points for each team
    #teams_played: a nested list of who's played what team

    #normalizing points for each team because some teams may have played more matches
    for i in range(len(points)):
        points[i] = points[i] / len(team_played[i])

    #putting all the information into a dictionary where team_id is the key
    #and points and team_played are values
    dic = {}
    for i in range(len(team_id)):
        if team_id[i] not in dic:
            dic[team_id[i]] = [points[i], team_played[i]]
    
    #sort dic based on points
    sorted_dic = dict(sorted(dic.items(), key = lambda item: item[1][0], reverse=True))
    team_one = []
    team_two = []
    for k1, v1 in sorted_dic.items():
        for k2, v2 in sorted_dic.items():
            if k1 not in team_one and k1 not in team_two and k2 not in team_one and k2 not in team_two: #making sure the team hasn't already been matched
                if k1 != k2: #can't match team to itself
                    if k2 not in v1[1]: #making sure they haven't played yet
                        team_one.append(k1)
                        team_two.append(k2)
                        break
    
    #if there are an odd number of teams
    for k, v, in sorted_dic.items():
        if k not in team_one and k not in team_two:
            counter = 0
            while True:
                if counter != len(team_id): #if the team has played every team already
                    random_team = random.randint(1, len(team_id)) #picks a random team
                    if random_team == k: #makes sure that random team isn't itself
                        counter += 1
                        continue #if it is itself, add one to counter and try again
                    team_one.append(k)
                    team_two.append(random_team)
                    break
                else: #if they have played every team, then they play the adjacent team
                    team_one.append(k)
                    try:
                        team_two.append(list(sorted_dic.keys())[k - 1])
                        break
                    except:
                        team_two.append(list(sorted_dic.keys())[k + 1])
                        break
    
    #creating dataframe
    #df = pd.DataFrame(list(zip(team_one, team_two)), columns = ["Team One", "Team Two"])
    return team_one, team_two

def contact_info(team_one, team_two):
    gc = gspread.service_account(filename='service_account.json')
    # Open a sheet from a spreadsheet in one go
    wks = gc.open('Team info').sheet1
    contact_df = wks.get_all_records()
    team_one_info = []
    team_two_info = []
    for i in range(len(team_one)):
        #team one info
        team = team_one[i]
        team_one_info.append((contact_df[team - 1]['Team Captian'], contact_df[team - 1]['Phone Number']))
        #team two info
        team = team_two[i]
        team_two_info.append((contact_df[team - 1]['Team Captian'], contact_df[team - 1]['Phone Number']))
    
    match_df = pd.DataFrame(list(zip(map(str, team_one_info), team_one, team_two, map(str, team_two_info))), columns = ["Team One Contact Info", "Team One", "Team Two", "Team Two Contact Info"])
    return match_df

'''Writing Weekly Matchups to Sheets'''
def weekly_matchups(df):
    gc = gspread.service_account(filename='service_account.json')
    # Open a sheet from a spreadsheet in one go
    wks = gc.open('Weekly Matches').sheet1
    wks.update('A1', "Week of " + str(date.today().strftime("%B %d") + "st Matches"))
    wks.update('A2', [df.columns.values.tolist()] + df.values.tolist())

def main():
    team_id, score, teams_played = get_data()
    team_one, team_two = match_making(team_id, score, teams_played)
    match_df = contact_info(team_one, team_two)
    weekly_matchups(match_df)
    print("Updated Weekly Matchups")
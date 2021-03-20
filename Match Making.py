import pandas as pd
import random

print('test')
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
    df = pd.DataFrame(list(zip(team_one, team_two)), columns = ["Team One", "Team Two"])
    return df

match_making([1,2,3,4,5,6,7], [1, 43, 2, 4, 5, 2, 0], [[2], [3, 5], [4], [5], [6, 2], [1], [6]])
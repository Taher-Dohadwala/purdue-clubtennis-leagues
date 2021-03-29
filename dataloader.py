
"""
Google Drive setup:

1. Score Reporting
2. Main
3. Weekly Matches
"""

"""
TODO:
1. read from score reporting and update main
2. Clear score reporting sheet
"""

import gspread
import pandas as pd



def read_reporting(sr):
    """Reads score reporting data, and parses the winner, loser, and score difference """
    winner = sr.col_values(2)[1:]
    loser = sr.col_values(3)[1:]
    score = sr.col_values(4)[1:]
    score_difference = [(int(x.split("-")[0])-int(x.split("-")[1])) for x in score]
    loser_score = [int(x.split("-")[1]) for x in score]

    return winner,loser,loser_score,score_difference

def nice_manual_check(winner,loser,loser_score,score_difference):
    for i in range(len(winner)):
        print(f"Team {winner[i]} won: Total score +{16}, Weighted Score +{score_difference[i]} and played {loser[i]}\nTeam {loser[i]} lost: Total Score +{loser_score[i]}, Weighted Score -{score_difference[i]} and played Team {winner[i]}")
    
def update_main(sr,main):
    winner,loser,loser_score,score_difference = read_reporting(sr)
    df = pd.DataFrame(main.get_all_records())
    df["Teams Played"] = df["Teams Played"].astype("string")
    print("Old Main")
    print(df)
    
    print("Expected Changes")
    nice_manual_check(winner,loser,loser_score,score_difference)
    
    for i in range(len(winner)):
        # update main for winning team
        prev_win = df.loc[df["Team Number"]==int(winner[i]),"Total Score"].values[0]
        df.loc[df["Team Number"] == int(winner[i]),"Total Score"] = prev_win + 16
        
        win_tp = df.loc[df["Team Number"]==int(winner[i]),"Teams Played"].values[0]
        df.loc[df["Team Number"] == int(winner[i]),"Teams Played"] = win_tp  + ","+ str(loser[i])
        
        prev_weighted_win = df.loc[df["Team Number"]==int(winner[i]),"Weighted Score"].values[0]
        df.loc[df["Team Number"] == int(winner[i]),"Weighted Score"] = prev_weighted_win + int(score_difference[i])
        
        
        #update main for losing team
        prev_lose = df.loc[df["Team Number"]==int(loser[i]),"Total Score"].values[0]
        df.loc[df["Team Number"] == int(loser[i]),"Total Score"] = prev_lose + int(loser_score[i])
        
        lose_tp = df.loc[df["Team Number"]==int(loser[i]),"Teams Played"].values[0]
        df.loc[df["Team Number"] == int(loser[i]),"Teams Played"] = lose_tp  + ","+ str(winner[i])
        
        prev_weighted_lose = df.loc[df["Team Number"]==int(loser[i]),"Weighted Score"].values[0]
        df.loc[df["Team Number"] == int(loser[i]),"Weighted Score"] = prev_weighted_lose - int(score_difference[i])
        
    print("New Main")
    print(df)
    
    change = False
    answer = input("Send changes to drive (y/n): ")
    if answer =="y":
        change = True
    if change:
        main.update([df.columns.values.tolist()] + df.values.tolist())
        print("main updated")
    else:
        print("Manually check new changes")
    
def clear_score_reporting(sr):
    answer = input("Confirm clearing score reporting (y/n): ")
    if answer =="y":
        print("Clearing")
        size = len(sr.col_values(1))
        for i in range(size-1):
            sr.delete_rows(2)
    else:
        print("Score Reporting NOT cleared")
        
    
def update_main_and_clear_sr(test=False):
    gc = gspread.service_account(filename='service_account.json')
    sr = gc.open('Score Reporting').get_worksheet(0)
    main = gc.open('Main').get_worksheet(0)
    
    update_main(sr,main)
    clear_score_reporting(sr)
    print("Ready for matchmaking")
    

if __name__ == "__main__":
    update_main_and_clear_sr()
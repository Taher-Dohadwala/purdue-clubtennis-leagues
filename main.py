from dataloader import update_main_and_clear_sr
from Match_Making import assign_matches_and_update_weeklymatches
import sys

if __name__ == "__main__":
    # First week of leagues
    if sys.argv[1] == "start":
        assign_matches_and_update_weeklymatches()
    # all other weeks of leagues
    else:
        update_main_and_clear_sr()
        assign_matches_and_update_weeklymatches()
    print("Finished")

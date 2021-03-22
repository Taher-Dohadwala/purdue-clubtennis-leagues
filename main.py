from dataloader import update_main_and_clear_sr
from Match_Making import assign_matches_and_update_weeklymatches

if __name__ == "__main__":
    update_main_and_clear_sr()
    assign_matches_and_update_weeklymatches()
    print("Finished")

# team id, point value, who they played

"""
Google Drive setup:

1. Team's setup sheet [x]
2. Team score reporting form


"""

"""
Read data in from google sheets

get team id, point value, who they played
"""

import gspread

#gc = gspread.service_account()
gc = gspread.service_account(filename='service_account.json')

# Open a sheet from a spreadsheet in one go
wks = gc.open('Team info').sheet1
df = wks.get_all_values()
print(df)
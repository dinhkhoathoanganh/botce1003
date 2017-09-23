import gspread
from oauth2client.service_account import ServiceAccountCredentials
 
 
# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('chipsmore-c90a7df667f6.json', scope)
client = gspread.authorize(creds)
 
# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
sheet = client.open("Canteen / Restaurant List").sheet1
 
# Extract and print all of the values
print(sheet.get_all_values())
# write 'Blue' to C2 cell
sheet.update_acell('C2', 'Blue')
# reading 
all_cells = sheet.range('A1:C6')
print(all_cells)
for cell in all_cells:
 print (cell.value)

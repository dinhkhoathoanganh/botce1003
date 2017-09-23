from openpyxl import load_workbook
#load wb from a file
wb = load_workbook('canteen_restaurant_list.xlsx')
#print sheets name
print wb.get_sheet_names()


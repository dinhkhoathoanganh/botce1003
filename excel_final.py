from openpyxl import load_workbook
import datetime
#load workbook from a file and grab the active worksheet
wb=load_workbook('canteen_restaurant_list.xlsx')
ws=wb.active

#return cell value function
def cellvalue(x): #x is the cell address(str)
 return ws[x].value

#save the file
def save_xl(x):
 wb.save("canteen_restaurant_list.xls")

#write datetime to cell
def write_datetime(x): #x is the cell address(str)
 ws[x] = datetime.datetime.now()

#assign data
def assign(x,y):
 ws[x]=y


from openpyxl import load_workbook
import datetime
#load workbook from a file and grab the active worksheet
work_book=load_workbook('canteen_restaurant_list.xlsx')
work_sheet=work_book.active

#return cell value function
def cellvalue(x): #x is the cell address(str)
 return work_sheet[x].value

#save the file
def save_xl(x):
 work_book.save("canteen_restaurant_list.xls")

#write datetime to cell
def write_datetime(x): #x is the cell address(str)
 work_sheet[x] = datetime.datetime.now()

#assign data
def assign(x,y):
 work_sheet[x]=y

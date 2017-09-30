from openpyxl import load_workbook

import datetime
#load workbook from a file and grab the active worksheet
work_book=load_workbook('canteen_restaurant_list.xlsx')
work_sheet=work_book['Sheet2'] #open 'Sheet2' <name of sheet>

#return cell value function
def cell_value(x): #x is the cell address(str)
 return work_sheet[x].value

#save the file
def save_xl(z): #z is the file name
 work_book.save(z)

#write datetime to cell
def write_datetime(x): #x is the cell address(str)
 work_sheet[x] = datetime.datetime.now()

#assign data
def assign(x,y): #x is the cell address(str)
 work_sheet[x]=y

#return column value
def column_value(x): #x is column addr (str)
 value_list = []
 for i in range(len(work_sheet[x])):
  if str(type(work_sheet[x][i].value)) != "<class 'NoneType'>":
   value_list = value_list + [work_sheet[x][i].value]
 return value_list

#return corresponding cell
def cor_value(x,y,z): #x,y is the column addr, z is the value (str, str)
 value_list = []
 for i in range(len(work_sheet[x])):
  if z == str(work_sheet[x][i].value):
   cell_rows = str(i + 1)
 return cell_value(y+cell_rows)

#program starts from here
assign('A1',20)
print(cor_value('A','B','banana'))
save_xl('canteen_restaurant_list.xlsx')


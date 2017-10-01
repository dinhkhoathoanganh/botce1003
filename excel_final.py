import openpyxl
import datetime

class xl:

 #load a workbook from file
 def load_wb(file_name): #file_name (str)
  return openpyxl.load_workbook(file_name)

 #load a worksheet from a worksheet
 def load_ws(work_book, ws_name): #ws_name (str)
  return work_book[ws_name]

 #save a workbook to file
 def save_wb(work_book, file_name):
  work_book.save(file_name)

 #return a cell content
 def cell(work_sheet, cell_addr):
  return work_sheet[cell_addr].value
 #assign data to a cell of a worksheet
 def assign(work_sheet, cell_addr, cell_content):
  work_sheet[cell_addr] = cell_content

 #return content of a column
 def column(work_sheet, column):
  content = []
  for i in range(len(work_sheet[column_addr])):
   if str(type(work_sheet[column_addr][i].value)) != "<class 'NoneType'>":
    content = content + [work_sheet[column_addr][i]]
  return content

 #return corresponding content
 def cor_content(work_sheet,column1, column2, cell1_value):
  content = []
  for i in range(len(work_sheet[column1])):
   if cell1_value == str(work_sheet[column1][i].value):
    cell_row = str(i + 1)
  return cell(column2 + cell_row)

#PROGRAM STARTS
mywb = xl.load_wb('test.xlsx')
myws = xl.load_ws(mywb,'test')
xl.assign(myws, 'C3', 'fuck you mom')
print(xl.cell(myws, 'C3'))
xl.save_wb(mywb,'test.xlsx')

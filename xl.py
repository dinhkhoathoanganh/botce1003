#updated by Anh
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

 #return a cell CONTENT #cells_addr str
 def cell(work_sheet, cell_addr):
  return str(work_sheet[cell_addr].value)

 #assign data to a cell of a worksheet
 def assign(work_sheet, cell_addr, cell_content):
  work_sheet[cell_addr] = cell_content

 #return CONTENT of a column #cot doc
 def column(work_sheet, column_addr):
  content_list = []
  for i in range(len(work_sheet[column_addr])):
   if str(type(work_sheet[column_addr][i].value)) != "<class 'NoneType'>":
    content_list = content_list + [work_sheet[column_addr][i].value]
  return content_list

 #return LIST of a column-range #row1,2 either string or int
 def col_range(work_sheet, column_addr, row1, row2):
  content = []
  for i in range(int(row1), int(row2)+1):
   if str(type(work_sheet[column_addr][i].value)) != "<class 'NoneType'>":
    content = content + [work_sheet[column_addr][i]]
  return content

 #return list of rows of a content 
 def rowlist(work_sheet, column_addr, content):
  for n in range(len(xl.column(work_sheet,column_addr))):
   if xl.column(work_sheet,column_addr)[n] == content:
    content2 = xl.column(work_sheet,column_addr)[n+1]
  for i in range(len(work_sheet[column_addr])):
   if str(work_sheet[column_addr][i].value) == content:
    row1 = i
   if str(work_sheet[column_addr][i].value) == content2:
    row2 = i
  return [row1,row2]


 #return corresponding content horizontally
 def cor_content(work_sheet,column1, column2, cell1_value):
  content = []
  for i in range(len(work_sheet[column1])):
   if cell1_value == str(work_sheet[column1][i].value):
    cell_row = str(i + 1)
  return xl.cell(work_sheet,column2 + cell_row)

 #return corresponding content vertically
 def cor_content_col(work_sheet,row1, row2, cell1_value):
  content = []
  for i in range(len(work_sheet[str(row1)])):
   if cell1_value == str(work_sheet[str(row1)][i].value):
    cell_col = chr(i + 65) #65 corresponds to A
  return xl.cell(work_sheet,cell_col + str(row2))


 #return stall name
 def stall(work_sheet, column1, column2, cell_value):
  for i in range(len(work_sheet[column1])):
   if cell_value == str(work_sheet[column1][i].value):
    row = i +1
  while str(type(work_sheet[column2][row-1].value)) == "<class 'NoneType'>":
   row = row -1
  return xl.cell(work_sheet, column2 + str(row))

 #return list of sheets
 def sheets(work_book):
  return work_book.get_sheet_names()

#SAMPLE

print('Excel has loaded!')


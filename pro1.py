import xlrd

t=input()
#print(type(t))
loc = ("output.xlsx") 
  
# To open Workbook 
wb = xlrd.open_workbook(loc) 
sheet = wb.sheet_by_index(0) 
s=sheet.cell_value(0,0)
#print(type(s))
#wb.close()
# For row 0 and column 0 
for i in range(1,17):
    s=sheet.cell_value(i,0)
    #print(type(s))
    #print(sheet.cell_value(i,1))
    if(s==t):
       print(sheet.cell_value(i,1))
       break
    #print(s.__eq__(t))
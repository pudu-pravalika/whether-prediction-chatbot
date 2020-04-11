
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
import nltk
import sqlite3
import xlrd 
import xlsxwriter 
j=1
# Give the location of the file 
loc = ("input.xlsx") 
  
# To open Workbook 
wb = xlrd.open_workbook(loc) 
sheet = wb.sheet_by_index(0) 
  
# For row 0 and column 0 
import xlwt 
from xlwt import Workbook 
  
# Workbook is created 
#wb = Workbook() 
workbook = xlsxwriter.Workbook('output.xlsx') 
sheet2 = workbook.add_worksheet() 
  
  
# add_sheet is used to create sheet. 
#sheet2 = wb.add_sheet('Sheet2') 
  
 
conn=sqlite3.connect("./test.db")
#Take an input and tokenize using nltk method
for i in range(1,61):
    sentence = sheet.cell_value(i, 0)
    sentence = sentence.lower()
    print(sentence)
    tokens = word_tokenize(sentence)
    token1 = []

    #Pre-defined Datasets to compute the output
    maximum = ["highest", "elevated", "escalated", "heightened", "increased", "raised", "up", "high", "higher", "high", "max", "increase", "increased"]
    avg = ["average", "avg", "intermediate", "mean", "median", "medium", "middle", "middling", "midsize", "moderate", "modest", "adequete", "normal", "popular", "regular", "routine", "usual"]
    minimum = ["fewest", "littlest", "lowest", "minimal", "minutest", "slightest", "smallest", "tiniest", "fewer", "lesser", "low", "minor", "modest", "slight", "small", "small"]
    everything = ["all", "whole", "everything", "aggregate"]
    stop_words = set(stopwords.words("english"))

    #Remove stop words and tagging the parts of speech
    for i in tokens:
         if i not in stop_words:
              token1.append(i)
    print(token1)
    token1 = nltk.pos_tag(token1)
    print(token1)
    length = len(token1)

#Defined list of parts of speech as lists
    common_nouns = []
    proper_nouns = []
    verbs = []
    determiners = []
    numbers = []
    adjectives = []

    #Classify into the pre-defined list of parts of speech
    for i in range(length):
        if token1[i][1] == "NN" or token1[i][1] == "NNS" :
               common_nouns.append(token1[i][0])
        elif token1[i][1] == "NNP" or token1[i][1] == "NNPS" :
               proper_nouns.append(token1[i][0])
        elif token1[i][1] == "VB" or token1[i][1] == "VBD" or token1[i][1] == "VBG" or token1[i][1] == "VBP" or token1[i][1] == "VBZ" :
               verbs.append(token1[i][0])
        elif token1[i][1] == "WDT" :
               determiners.append(token1[i][0])
        elif token1[i][1] == "CD" :
               numbers.append(token1[i][0])
        elif token1[i][1] == "JJ" or token1[i][1] == "JJR" or token1[i][1] == "JJS" :
               adjectives.append(token1[i][0])

    numbers.sort()

    #Compute the adjectives from the pre-defined datasets and compute the query as per the requirements of the end user
    if len(adjectives) > 0 and len(adjectives) <= 1 :
          if adjectives[0] in maximum :
               sheet2.write(j,0, "SELECT MAX(temperature) from sensor ")
               #j=j+1
          elif adjectives[0] in avg :
               sheet2.write(j,0,"SELECT AVG(temperature) from sensor ")
               #j=j+1
          elif adjectives[0] in minimum :
               sheet2.write(j,0,"SELECT MIN(temperature) from sensor ")
               #j=j+1
          elif adjectives[0] in everything :
               sheet2.write(j,0, "SELECT * from sensor ")
               #j=j+1
          else:
               sheet2.write(j,0,"Could not generate query !")
               #j=j+1
    elif len(adjectives) > 1:
        print("More than two inputs given, will process the first one.")
        if adjectives[0] in maximum :
            output = "SELECT MAX(temperature) from table_name "
            #j=j+1
        elif adjectives[0] in avg :
            output = "SELECT AVG(temperature) from table_name "
            #j=j+1
        elif adjectives[0] in minimum :
            output = "SELECT MIN(temperature) from table_name "
            #j=j+1
        elif adjectives[0] in everything :
            output = "SELECT * from table_name"
            #j=j+1
        else:
            output = "Could not generate query !"
            #j=j+1

    else:
       output = "SELECT temp from sensor"
    
   #This part of the code handles the remaining part of the query 
    if len(numbers) == 1 :
        print(output +  " where time = " + numbers[0])
        sheet2.write(j,0,output +  " where time = " + numbers[0])
        #j=j+1

    elif len(numbers) == 2:
        print(output + " where time between " + numbers[0] + " and " + numbers[1])
        sheet2.write(j,0,output + " where time between " + numbers[0] + " and " + numbers[1])
        #j=j+1
        
    elif len(numbers) == 0:
        print("SELECT temp from sensor where day = 5")
        sheet2.write(j,0,"SELECT temp from sensor where day = 5");
        #j=j+1
      
    else:
       print("could not genterate query")
       sheet2.write(j,0,"Could not generate query");
       
    j=j+1
#workbook.save('output.xlsx')
workbook.close()


#This is the code saved for later use.
#date0 = ["past", "yesterday"]
#date1 = ["today", "present", "currently", "presently", "now", "later"]
#date2 = ["tomorrow", "future"]
#day = ["afternoon", "evening", "morning", "night"]
#print(output)
#print(common_nouns)
#print(proper_nouns)
#print(verbs)
#print(determiners)
#print(numbers)
#print(adjectives)
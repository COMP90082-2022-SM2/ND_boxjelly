# https://betterprogramming.pub/how-to-convert-pdfs-into-searchable-key-words-with-python-85aab86c544f
import PyPDF2
import textract
# import camelot.io as camelot
filename = '/Users/sophiezheng/Desktop/ND_boxjelly/PBSP.pdf'
import fitz
import pandas as pd 

from tabula import read_pdf
from tabulate import tabulate
import pandas as pd
import io

# Read the only the page n°6 of the file
tables = read_pdf(filename,pages = 5, pandas_options={'header': None},
                         multiple_tables = True, stream = True)

# Transform the result into a string table format
table = tabulate(tables)
print("table:", table)
print("table:", tables[0].values.tolist())
# Transform the table into dataframe
df = pd.read_fwf(io.StringIO(table))
print(df)
# df.to_excel("pdf_to_table.xlsx")
"""
pdfFileObj = open(filename,'rb')

pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

num_pages = pdfReader.numPages
count = 0
text = ""
#The while loop will read each page.
while count < num_pages:
    pageObj = pdfReader.getPage(count)
    count +=1
    print("text: ", pageObj.extractText())
    text += pageObj.extractText()

#This if statement exists to check if the above library returned words. It's done because PyPDF2 cannot read scanned files.
if text != "":
   text = text
#If the above returns as False, we run the OCR library textract to #convert scanned/image based PDF files into text.
else:
   text = textract.process(fileurl, method='tesseract', language='eng')
   # print("text: ", text)
"""
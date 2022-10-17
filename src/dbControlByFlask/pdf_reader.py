from tabula import read_pdf
# extract text with open - to html
# %pip3 install pdfminer.six
from io import StringIO
from pdfminer.high_level import extract_text_to_fp
from pdfminer.layout import LAParams

from bs4 import BeautifulSoup

page_info = {1: {"continuous": True, "next_page":False}, 3: {"continuous": False, "next_page":False}, 
    4: {"continuous": False, "next_page":False}, 5: {"continuous": True, "next_page":True}, 
    7: {"continuous": False, "next_page":True}, 9: {"continuous": False, "next_page":True}, 
            10: {"continuous": False, "next_page":True}, 11: {"continuous": False, "next_page":True}, 
            12: {"continuous": False, "next_page":False}, 13: {"continuous": False, "next_page":False}, 
            14: {"continuous": False, "next_page":False}}

output_string = StringIO()

with open('PBSP Summary Document Final.pdf', 'rb') as fin:
    extract_text_to_fp(fin, output_string, laparams=LAParams(),output_type='html', codec=None)

output = output_string.getvalue().strip()
# print(output)
soup = BeautifulSoup(output, "html5lib")

bolded = soup.find_all("span", {"style": "font-family: Calibri-Bold; font-size:11px"})
bolded_lst = [p.getText(strip=True) for p in bolded]
print(bolded_lst)

def table_extraction(page_num):
    filename = "PBSP Summary Document Final.pdf"

    # Read the only the page no.4 of the file
    tables = read_pdf(filename, pages=page_num, pandas_options={'header': None},
                      multiple_tables=True, stream=True, lattice=True)

    # Transform the result into a string table format
    table_lists = []
    for table in tables:
        lists = [list(filter(lambda x: x == x, inner_list)) for inner_list in
                 table.values.tolist()]  # delete all nan values
        table_lists.append([e for e in lists if e])  # filter out empty lists
    return table_lists

def extract_answers(table_lists):
    answers_all = []
    sub_col_answers_all = []
    for table in table_lists:
        i = 1
        answers = []
        sub_col_answers = []
        while i < len(table):
            if len(table[i]) == 1:
                answers.append(str(table[i]))
                #print("answers:", str(table[i])) #first index: how many tables in that page
                i+=1
            elif len(table[i]) > 1: 
                if len(table[i-1]) == 1:
                    if i+1 == len(table) or len(table[i+1]) == 1:
                        bolded_element = list(set(table[i]).intersection(bolded_lst))
                        if bolded_element: 
                            answers.append(bolded_element[0])
                        else: 
                            answers.append(str(table[i]))
                        i+=1
                    else:
                        sub_col_answers.append(table[i])
                        if i+1 == len(table) or len(table[i+1]) == 1:
                            if sub_col_answers:
                                #print("``````", sub_col_answers)
                                sub_col_answers_all.append(sub_col_answers) # the end of the sub-col table
                                sub_col_answers = []
                            i+=1                         
                else:
                    if i+1 != len(table) and len(table[i+1]) > 1: #multi-sub-col/sub-col table
                        sub_col_answers.append(table[i])
                    elif i+1 == len(table) or len(table[i+1]) == 1:
                        sub_col_answers.append(table[i])
                        if sub_col_answers:
                            #print("~~~~~~~`", sub_col_answers)
                            sub_col_answers_all.append(sub_col_answers) # the end of the sub-col table
                            sub_col_answers = []
                        i+=1
            i+=1
        if len(answers) != 0:
            answers_all.append(answers)
        if len(sub_col_answers) != 0:
            #print("************", i, sub_col_answers)
            sub_col_answers_all.append(sub_col_answers) # the end of a whole table
    return answers_all, sub_col_answers_all
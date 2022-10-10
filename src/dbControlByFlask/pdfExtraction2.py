import pdfplumber
import pandas as pd
import fitz
import copy

def get_pdf_content(file_name):
    doc = fitz.open(file_name)
    text = {}
    for i in range(doc.page_count):
        page = doc[i]
        text[i] = page.get_text()

    dict_pdf = {}
    all_content = ""
    for i in text.keys():

        if "Commented [" in text[i]:
            comment_start_position = text[i].find("Commented [")
            dict_pdf[i] = {"content": text[i][:comment_start_position], "comment": text[i][comment_start_position:]}
            all_content += text[i][:comment_start_position]
        else:
            all_content += text[i]

    pdf = pdfplumber.open(file_name)
    tables = []
    bolds = []
    for page in pdf.pages:
        # Gets all text information for the current page, including text in a table
        for table in page.extract_tables():
            for row in table:
                tables.append(row)
        clean_text = page.filter(lambda obj: obj["object_type"] == "char" and "Bold" in obj["fontname"])
        t = clean_text.extract_text()
        if t:
            bolds.append(t.replace('\n',' '))
    # dict_pdf is a dictionary whose key is the number of the page and values are also dictionary which contains keys of "content" and "comment"
    # all_content is a string which contains all the text except the comments
    # tables is a list and the item is the list form of lines, this is used to extract content in tables
    return dict_pdf,all_content.replace("\n"," "),tables,bolds

def extract_paragraph(start_string,end_string,all_content):
    start = all_content.find(start_string)
    end = all_content.find(end_string)
    current_content = all_content[start+len(start_string):end]
    return current_content

def extract_paragraph_given_start(start_string,end_string,all_content,start_position):
    all_content_copy = copy.deepcopy(all_content[start_position:])
    print(all_content_copy)
    start = all_content_copy.find(start_string)
    end = all_content_copy.find(end_string)
    current_content = all_content_copy[start+len(start_string):end]
    return (current_content,end+start_position)


def extract_table(s,e,tables,start_index):
    cur_table = []

    for i in range(start_index,len(tables)):
        try:
            if s in tables[i]:
                i+=1
                if len(list(filter(None, tables[i]))) == 0:
                    print("*************************************************")
                    i+=1
                table_length = len(list(filter(None, tables[i])))
                index = i+1
                while e not in tables[index]:
                    temp = []
                    for j in tables[index]:
                        if isinstance(j, str):
                            temp.append(j)
                    if len(temp) == table_length:
                        cur_table.append(temp)
                    # if the current length is smaller than number of table columns, add the cuurent text to the previous one

                    index+=1
                return((cur_table),index)
        except:
            print("search table failed")
    print("cannot find "+s)
from tabula import read_pdf
page_info = {1: {"continuous": False, "next_page":True}, 3: {"continuous": False, "next_page":False}, 
    4: {"continuous": False, "next_page":False}, 5: {"continuous": True, "next_page":True}, 
    7: {"continuous": False, "next_page":True}}


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
    print(table_lists[0])
    return table_lists

def extract_answers(table_lists):
    answers_all = []
    for table in table_lists:
        i = 1
        answers = []
        while i < len(table):
            if len(table[i-1]) == 1 and len(table[i]) == 1:
                answers.append(str(table[i]))
                # print(table[i]) #first index: how many tables in that page
                i+=1
            else:
                if len(table) == 2: #sub-col name - value
                    # insert the value as attribute directly
                    print("aaa")
                else:
                    # insert to another table
                    print("bbb", table[i])
            i+=1
        if len(answers) != 0:
            answers_all.append(answers)
    return answers_all

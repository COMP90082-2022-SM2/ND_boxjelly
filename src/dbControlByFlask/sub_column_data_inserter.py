from data_inserter import data_insert
# please refer to "PDF Extraction" in Implementation tag
# ref_table: Every multi-column-contained tables' foreign key reference to another table's primary key
ref_table = {"persons_consulted": "assessment", "STC": "ba_function", "medication": "chemical_restraint", 
             "chemical_restraint": "intervention", "physical_restraint": "intervention", 
             "mechanical_restraint": "intervention", "environmental_restraint": "intervention", 
            "social_validity1": "chemical_restraint", "authorisation1": "chemical_restraint", 
            "social_validity2": "physical_restraint", "authorisation2": "physical_restraint", 
            "social_validity3": "mechanical_restraint", "authorisation3": "mechanical_restraint", 
            "social_validity4": "environmental_restraint", "authorisation4": "environmental_restraint", 
            "social_validity5": "seclusion_restraint", "authorisation5": "seclusion_restraint", 
            "how_implementer": "implementation", "implementation_plan": "implementation", "how_communicate": "implementation", 
            "how_implementation": "implementation"}

def sub_column_data_insert(mydb, cur, page_num, sub_column_table_info, sub_col_answers_all):
    """
    inserting multi-columned data to database
    """
    for sub_table_j in range(len(sub_column_table_info[page_num])): 
        sub_attributes = ""
        fk = False

        for sub_attr in sub_col_answers_all[sub_table_j][0]:
            sub_attr = sub_attr.replace('(', '').replace(')', '')
            if sub_attr[:3].lower() == 'how' or sub_attr[:3].lower() == 'who':
                attr = sub_attr[:3].lower()
            else:
                attr = ' '.join(elem.capitalize() for elem in sub_attr.split()).replace(" ", "")
                attr = attr[0].lower() + attr[1:]
            sub_attributes += attr
            sub_attributes += ", "
        
        if sub_column_table_info[page_num][sub_table_j] in ref_table:
            fk = True
            ref_table_name = ref_table[sub_column_table_info[page_num][sub_table_j]]
            fk_name = ref_table_name.lower() + "_id"
            sql = "SELECT MIN(id) FROM " + ref_table_name
            cur.execute(sql)
            f_k_id = int(cur.fetchall()[0][0])
            fk_val = (f_k_id, ) 
            sub_attr_final = fk_name + ", " + sub_attributes[:-2]
        for row in sub_col_answers_all[sub_table_j][1:]:
            row = [ele.replace('\r', ' ').replace(r'\r', ' ') for ele in row]
            if fk:
                data_insert(mydb, cur, sub_column_table_info[page_num][sub_table_j], sub_attr_final, fk_val + tuple(row, ))
                
            else: #social_v table
                data_insert(mydb, cur, sub_column_table_info[page_num][sub_table_j], sub_attr_final, tuple(row, ))
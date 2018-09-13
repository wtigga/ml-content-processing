# coding: utf-8
import csv

from langdetect import detect
file_output = 'pushes_analyzed.csv'  # file two write sorted messages to
file_input = 'pushes_2018-09-11_all.csv'  # file to read messages from
# list of column names with languages
fields = ['Key', 'en', 'es', 'pt', 'fr', 'de', 'it', 'ru', 'ja', 'kr','ar','tr','th','vi','nl','he','in','pl','uk','id']
# list where rows are stored
strings_list = []
# reader of cv in dict format with dialect delimiter set to tabulation
dict_reader = csv.DictReader(open(file_input), dialect='excel-tab')
# function to analyze language of the string
def language_detection(reader, fld, key_reading, content_reading, str_lst):
    # reader is the dict_reader from above
    # fld is list of column names stored in fields
    # key_reading is the name of the Key column where ID or key is stored
    # content_reading is the column name to read language for analysis
    # str_lst is the target string list to write rows to
    for row in reader:
        current_content = row[content_reading]  # pick the string to analyze language
        try:
            current_content = current_content.strip("'")  # clean garbage from strings
            current_content = current_content.strip('"')  # clean garbage from strings
            current_content = current_content.strip()  # clean garbage from strings
        except AttributeError:
            pass
        current_key = row[key_reading]  # remember the key or id
        try:  # in case langdetect can't recognize language
            current_lang = detect(current_content)  # recognizing language
            if current_lang in fld:  # check if the language is in the list of column names, otherwise ignore it
                                    # to filter out unnescessary languages completely
                print(current_key, 'identified as', current_lang)
                current_entry = {key_reading: current_key, current_lang: current_content}   # create a row with two columns - key with key, and recognized language code with content
                full_row = {**row, **current_entry}  # combine all original row with recognized language
                full_row.pop(content_reading)  # remove the column with content to recognize
                str_lst.append(full_row)  # add a row to the list of strings
            else:
                pass
        except:
            print('Something wrong with identification of: ', current_key)
def write_to_csv(str_lst, output, dlct='excel-tab'):
    with open(output, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields, dialect=dlct)
        writer.writeheader()
        writer.writerows(str_lst)
language_detection(dict_reader, fields, 'Key', 'content', strings_list)
write_to_csv(strings_list, file_output)


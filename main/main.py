# coding: utf-8
import csv  # to process input and output files
from langdetect import detect  # module to detect languages
from os import path  # to check if file exists

file_input = 0  # file to read messages from
list_of_langs = open("language_codes.txt")  # files with language list
fields = list_of_langs.read().rsplit(',')  # processed list of languages

# asking user to provide source file name
nextstep = 0
while nextstep == 0:
    print('Please input CSV file name to process\nor NONE (all caps) to quit')
    request_input_name = input('>>> ')
    if request_input_name == 'NONE':
        print('Bye!')
        quit('quitting....')
    elif path.exists(str(request_input_name + '.csv')) is True:
        file_input = str(request_input_name + '.csv')
        nextstep = 1
    else:
        print('File not found, try again')


file_output = (file_input + '_sorted.csv')  # file two write sorted messages to

strings_list = []  # list where rows are stored

# reader of cv in dict format with dialect delimiter set to tabulation
dict_reader = csv.DictReader(open(file_input), dialect='excel-tab')


def content_clenaup(incoming_string):  # cleaning string from garbage symbols
    incoming_string = str(incoming_string)
    try:
        incoming_string = incoming_string.strip("'")
    except: pass
    try:
        incoming_string = incoming_string.strip('"')
    except: pass
    try:
        incoming_string = incoming_string.strip()
    except: pass
    try:
        incoming_string = incoming_string.strip('"')
    except: pass
    try:
        incoming_string = incoming_string.replace('【', '[')
    except: pass
    try:
        incoming_string = incoming_string.replace('】', ']')
    except: pass
    try:
        incoming_string = incoming_string.replace('！', '!')
    except: pass
    try:
        incoming_string = incoming_string.replace('？', '?')
    except: pass
    return(incoming_string)


# receive content with ID (key), return a dict with ID and content under language code
def detect_and_return(string_of_content, source_key='source'):
    output = {}
    try:
        content = content_clenaup(string_of_content.get(source_key))
    except AttributeError:
        print('Input must be dict')
        quit()
    try:
        id_of_string = string_of_content.get('ID')
    except AttributeError:
        print('Input must be dict')
        quit()
    try:
        lang = detect(content)
        output = {'ID': id_of_string, lang: content}
    except:
        print('Error identifying {}'.format(id_of_string))
    return output


def language_detection_2(reader, content_column_name):
    output_list = []
    for row in reader:
        row_original = row
        row_detected = detect_and_return(row, content_column_name)
        row_combined = {**row_original, **row_detected}
        output_list.append(row_combined)
    return output_list


# function to analyze language of the string
def language_detection(reader, fld, key_reading, content_column_name, str_lst):
    # reader is the dict_reader from above
    # fld is list of column names stored in fields
    # key_reading is the name of the Key column where ID or key is stored
    # content_reading is the column name to read language for analysis
    # str_lst is the target string list to write rows to
    for row in reader:
        current_content = row[content_column_name]  # pick the string to analyze language
        current_key = row[key_reading]  # remember the key or id
        current_content = content_clenaup(current_content)  # using string clean to remove garbage
        try:  # in case langdetect can't recognize language
            current_lang = detect(current_content)  # recognizing language
            if current_lang in fld:  # check if the language is in the list of column names, otherwise ignore it
                                    # to filter out unnescessary languages completely
                print(current_key, 'identified as', current_lang)
                current_entry = {key_reading: current_key, current_lang: current_content}  # create a row with two columns - key with key, and recognized language code with content
                full_row = {**row, **current_entry}  # combine all original row with recognized language
                full_row.pop(content_column_name)  # remove the column with content to recognize
                str_lst.append(full_row)  # add a row to the list of strings
            else:
                pass
        except:
            print('Something wrong with identification of: ', current_key)


def write_to_csv(str_lst, output, dlct='excel-tab'):
    with open(output, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields, dialect=dlct, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(str_lst)


# executing the program
#language_detection(dict_reader, fields, 'ID', 'source', strings_list)

strings_list = language_detection_2(dict_reader, 'source')
write_to_csv(strings_list, file_output)
quit('Done.')


import os
import csv


# ======================================================================================================================
# Name:
#               get_dictionaries()
# Purpose:
#               Returns a list of strings that represent paths
#               where files were found with file names within dictionaries directory
# ======================================================================================================================
def get_dictionaries(dict_type="allowed_dictionaries"):
    main_dir_path = os.getcwd()  # get current working directory (main directory of script that is run)
    dict_path = os.path.join(main_dir_path, "resources", "dictionaries", dict_type)
    # creates path for dictionaries from main directory
    # dict_type = "dictionaries" or director name
    path_triple = (next(os.walk(dict_path)))  # generates triple with [path, directories and files]
    file_list_paths = []
    dir_path = path_triple[0]  # directory path
    top_files = path_triple[2]  # file names

    for file_name in top_files:  # for each file in a list of files
        full_path = (os.path.join(dir_path, file_name))  # create full path for that file
        file_list_paths.append(full_path)  # append path to the file list

    return file_list_paths  # returns all paths


# ======================================================================================================================
# Name:
#               extract_dictionaries(dictionaries_paths)
# Purpose:
#               Returns a dictionary of dictionary file with name of dictionary file and all words within it
# Arguments:
#               A list of strings with paths to files to be opened
# ======================================================================================================================
def extract_dictionaries(dictionaries_paths):
    all_dictionaries = dict()  # creates new dictionary
    for dictionary_path in dictionaries_paths:  # For each file path in a list of file paths
        tmp_dict_content = []  # empty list to prevent errors
        tmp_dict_name = os.path.basename(dictionary_path)  # extracts filename from path
        try:
            with open(dictionary_path) as f:
                tmp_dict_content = f.read().splitlines()  # splits contents of the file line by line into a list
                tmp_dict_content = list(set(tmp_dict_content))  # remove duplicates from the list
                tmp_dict_content.sort()  # sort list alphabetically
        except IOError as e:
            pass
            print("Error encountered during opening a dictionary file: " + str(e))

        all_dictionaries[tmp_dict_name] = tmp_dict_content  # assigns new dictionary key and list of words as value
    return all_dictionaries  # returns dictionaries


# ======================================================================================================================
# Name:
#               load_dictionaries()
# Purpose:
#               function to be called to link get_dictionaries() and extract_dictionaries(dictionaries_paths)
# ======================================================================================================================
def load_dictionaries(dict_type="allowed_dictionaries"):
    dictionaries_paths = get_dictionaries(dict_type)
    # retrieves paths for all dictionaries within dictionaries directory
    all_dictionaries = extract_dictionaries(dictionaries_paths)  # holds dictionaries
    return all_dictionaries


# =============================================================================
# Name:       generate_recursive_file_list()
# Purpose:    Returns a list of strings that represent paths where files were found with file names
# =============================================================================
def generate_recursive_file_list(input_path):
    import os
    list_of_files = []
    for dir_path, directories, files in os.walk(input_path):
        for file_name in files:
            full_path = (os.path.join(dir_path, file_name))
            list_of_files.append(full_path)  # appends directly to list
    return list_of_files


# ======================================================================================================================
# Name:
#               file_to_lines(file_path)
# Purpose:
#               Returns a list of lines loaded from a file
# Arguments:
#               A  strings with path to file
# ======================================================================================================================
def file_to_lines(file_path):

    lines = []
    try:
        #with open(file_path) as f:
        with open(file_path, encoding='utf-8') as f:
            # Added encoding to see if i can remove UnicodeDecodeError as in
            # http://stackoverflow.com/questions/12752313/unicodedecodeerror-in-python-3-when-importing-a-csv-file
            # as suggested http://stackoverflow.com/questions/2396238/memory-error-due-to-the-huge-input-file-size
            for line in f:
                lines.append(line.rstrip("\n")) # try that for memory issues
            #f.read().splitlines() could not handle it in memory?
            #lines = f.read().splitlines()  # splits contents of the file line by line into a list
    except IOError as e:
        # print("Error encountered during opening : " + file_path + " with error: " + str(e))
        pass
        # ignore errors for now are those are very likely and are not important at that stage
    except UnicodeDecodeError as ee:
        import tagpy
        short_file_name = os.path.relpath(file_path, os.path.split(tagpy.user_input)[0])  # TODO seperate settings (file)
        #print("UnicodeDecodeError - passing file: "+short_file_name)
        print(str(ee)+" - passing file: "+ short_file_name) #TODO output this to the log of errors...
        pass
    return lines


# ======================================================================================================================
# Name:
#               save_nested_list_to_csv(file_name, list)
# Purpose:
#               Returns a list of lines loaded from a file
# Arguments:
#               file_name - name for the .csv file to be saved under
#               list_for_csv - a nested list to be saved as csv file
# ======================================================================================================================
def save_to_csv(file_name, list_for_csv):
    my_file = open(file_name + ".csv", 'w', encoding='utf-8') # encoding seems to be required to correctly save results
    wr = csv.writer(my_file, quoting=csv.QUOTE_ALL)
    wr.writerows(list_for_csv)


# ======================================================================================================================
# Name:
#               save_to_file(file_name, data=None)
# Purpose:
#               Creates a file with filename and extension if no data is supplied. Data is written if supplied
# Arguments:
#               String containing name for the file to be created
# ======================================================================================================================
def save_to_file(file_name, extension, data=None):
    try:
        f = open(file_name+"."+extension, 'w', encoding='utf-8') # encoding seems to be required to correctly save results
        if data:
            for line in data:
                f.write(line)
                f.write('\n')
        f.close()
    except IOError:
        print("there was a problem with saving to a file")


# ======================================================================================================================
# Name:
#               generate_html_table(data_for_table)
# Purpose:
#               Returns a list of lines corresponding to html table with data from argument
# Arguments:
#               data_for_table - data to be inserted within the HTML code
# ======================================================================================================================
def generate_html_table(data_for_table):
    html_table = []
    html_table.append("<table class=\"sortable\">")
    html_table.append("    <thead>")

    table_labels = "        <tr>"
    for column in data_for_table[0]:
        table_labels += "<th>"+str(column)+"</th>"
    table_labels += "</tr>"

    html_table.append(table_labels)
    html_table.append("    </thead>")
    html_table.append("")
    html_table.append("    <tbody>")
    # starts from position 1 - as in skips first entry while [:-1] skips last entry
    for row in data_for_table[1:]:
        tmp_row = "        <tr>"
        for column in row:
            tmp_row += "<td>" + str(column) + "</td>"
        tmp_row += "</tr>"
        html_table.append(tmp_row)
    html_table.append("    </tbody>")
    html_table.append("</table>")
    return html_table


# ======================================================================================================================
# Name:
#               html_styles()
# Purpose:
#               Returns a list of lines corresponding to HTML style
# ======================================================================================================================
def html_styles():
    html_styles = []

    html_styles.append("<style>")
    html_styles.append("table {")
    html_styles.append("    font-family: arial, sans-serif;")
    html_styles.append("    font-size:	12px;")
    html_styles.append("    border-collapse: collapse;")
    html_styles.append("    width: 100%;")
    html_styles.append("}")
    html_styles.append("")
    html_styles.append("td, th {")
    html_styles.append("    border: 1px solid #000000;")
    html_styles.append("    text-align: left;")
    html_styles.append("    padding: 8px;")
    html_styles.append("}")
    html_styles.append("")
    html_styles.append("tr:nth-child(even) {")
    html_styles.append("    background-color: #E9E8E2;")
    html_styles.append("}")
    html_styles.append("mark {")
    html_styles.append("    background-color: #8D38C9;")
    html_styles.append("    color: yellow;")
    html_styles.append("}")
    html_styles.append("</style>")

    return html_styles


# ======================================================================================================================
# Name:
#               generate_html_page(html_table)
# Purpose:
#               Returns a list of lines corresponding to complete html page
# Arguments:
#               data_for_table - data to be inserted within the HTML code
# ======================================================================================================================
def generate_html_page(html_table):
    html_page = []
    html_page.append("<!DOCTYPE html>")
    html_page.append("<html>")
    html_page.append("<head>")
    html_page.append("<script src=\"sorttable.js\"></script>")
    html_page.append("")

    html_page.extend(html_styles())  # table with results

    html_page.append("")
    html_page.append("</head>")
    html_page.append("<body>")
    html_page.append("")

    html_page.extend(html_table)  # table with results

    html_page.append("")
    html_page.append("</body>")

    html_page.append("</html>")

    return html_page

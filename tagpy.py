#!/usr/bin/python3
import modules_tagpy.file_handling as file_handle
import os
import html
from time import localtime, strftime
from shutil import copyfile
import modules_tagpy.user_input as user_in

# ======================================================================================================================
# Global variables
# ======================================================================================================================
# get user_input for path - make sure its directory

creation_time = str(strftime("%Y-%m-%d@%H-%M-%S", localtime()))  # get datetime in format YYYY-MM-DD-HH-MM-SS

user_input = user_in.args.target

# loading all_dictionaries,all_banned_dictionaries and their respective values
all_dictionaries = file_handle.load_dictionaries()
all_banned_dictionaries = file_handle.load_dictionaries("banned_dictionaries")

# list of all files in the directory
all_files_to_search = file_handle.generate_recursive_file_list(user_input)  # All files to be checked with absolute path


# ======================================================================================================================
# =============================================================================
# Name:       generate_results()
# Purpose:    generate_results() returns nested list with results for file search
# =============================================================================
def generate_results():
    # list_of_all_lists - is a nested list which will hold values for each tab:
    # ["Dictionary Name", "Searched Item", "File Name", "Line Number", "Line Content"]
    # all_results = [["Dictionary Name", "Searched Item", "File Name", "Line Number", "Line"]]
    # all_results = [["Line Number", "Line", "Searched Item", "Dictionary Name", "File Name"]]
    all_results = [["Dictionary", "Searched", "Line", "Line Contents", "File Name"]]

    for each_file in all_files_to_search:  # goes through each file in the list of files with absolute paths

        # os.path.split(user_input) splits path into two parts (path - last element)
        short_file_name = os.path.relpath(each_file, os.path.split(user_input)[0])
        # short file name/path generated relative to the last directory in user_input

        # DICTIONARIES
        for dictionary in all_dictionaries:  # for each dictionary in list of dictionaries
            words = all_dictionaries[dictionary]  # words should contain all values from each of the dictionary file
            banned_words = []  # an empty list for banned words, in case no banned_dictionary is available
            try:
                banned_words = all_banned_dictionaries[dictionary]  # loads banned words for specific dictionary
            except:  # TODO Fix broad clause - not having one banned dictionary
                pass

            # KEY WORDS / STRINGS
            for word in words:  # for each word in list of words
                lines = file_handle.file_to_lines(each_file)  # lines from the files loaded into list
                line_count = 0  # line count should reset after each word is complete
                for line in lines:  # for each line within the list of lines
                    line_count += 1  # increment line position
                    if any(banned_word.lower() in line.lower() for banned_word in banned_words):
                        # if any of banned words are detected within the line - ignore that line as
                        # there is no point in doing additional detection
                        pass
                    elif word.lower() in line.lower():  # if word is found within the line - case insensitive
                        # all_results.append([dictionary, word, short_file_name, line_count, line])
                        # all_results.append([line_count, line, word, dictionary, short_file_name])
                        all_results.append([dictionary, word, line_count, line, short_file_name])

                        # append dictionary name, word within dictionary,
                        # shortened file name/path, line number in file, contents of that line
    return all_results


# ======================================================================================================================
# Name:
#               highlight_searched_in_contents(all_results)
# Purpose:
#               Returns a HTML ready list of lines with highlighted words for row of data
# Arguments:
#               all_results - Nested list (Table) of values found during search
# ======================================================================================================================
def highlight_searched_in_contents(all_results):  # TODO get a better way than 'string match'
    import re
    # identify searched column
    searched_column_index = None
    # identify content column
    content_column_index = None

    # first row of the results
    label_row = all_results[0]

    # counter to keep track of column number
    column_count = 0
    # set searched_column_index and content_column_index when words are found
    for column in label_row:
        if "Searched" in column:
            searched_column_index = column_count
        elif "Line Contents" in column:
            content_column_index = column_count
        column_count += 1
    # print("Searched = " + str(searched_column_index))
    # print("Content = " + str(content_column_index))

    # HTML preparation and highlighting
    for row in all_results:  # for each row in results

        row[content_column_index] = html.escape(row[content_column_index], quote=True)
        # prepare contents of "content_column_index" to be displayed in HTML page by escaping characters
        # Convert the characters &, < and > in string s to HTML-safe sequences.
        # https://docs.python.org/3/library/html.html#html.unescape

        regex_search = re.compile("(?i)(%s)" % row[searched_column_index])
        # creates a regex - case insensitive of searched value for that row.

        row[content_column_index] = re.sub(regex_search, r"<b><mark>\1</mark></b>",
                                           row[content_column_index])
        # inserts HTML tags to highlight found item

    return all_results


# TODO comments
def get_directory_name():
    # dir_base_name = os.path.split(user_input)[1]
    dir_base_name = os.path.basename(os.path.dirname(user_input))
    return str(dir_base_name) + "_" + str(creation_time)


def run_app():
    # list of lists with results for each file
    print("Generating all results!")
    list_of_all_results = generate_results()  # all found results

    # html_table = file_handle.generate_html_table(list_of_all_results)  #  generate a table for use with html page
    print("Highlighting HTML code!")
    highlighted_results = highlight_searched_in_contents(list_of_all_results)
    # prepare strings for HTML code and highlight items
    print("Generating HTML table!")
    html_table = file_handle.generate_html_table(highlighted_results)  # generate a table for use with HTML page
    print("Generating HTML page!")
    html_page = file_handle.generate_html_page(html_table)  # generate entire page as list of strings

    directory = os.path.join("results", get_directory_name())
    os.makedirs(directory, exist_ok=True)
    print("Saving HTML page!")
    file_handle.save_to_file(os.path.join(directory, "sortable_results"), "html", html_page)
    # generate a .html file with all found results in table
    print("Saving CSV file!")
    file_handle.save_to_csv(os.path.join(directory, "results"), list_of_all_results)
    # generate a .csv file with all found results

    copyfile(os.path.join("resources", "js", "sorttable.js"), os.path.join(directory, "sorttable.js"))

# =============================================================================
# Name:       main
# Purpose:    runsApp() and listens for keyboard interrupt to end script
# =============================================================================
if __name__ == '__main__':
    try:
        run_app()
    except KeyboardInterrupt:
        import sys
        print("\n\n{*} User Requested An Interrupt!")
        print("{*} Application Shutting Down.")
        sys.exit(1)
# =============================================================================
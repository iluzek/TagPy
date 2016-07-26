import re

global_lines = ""
global_file = ""

# *****************************************************************************
# =============================================================================
# Name:       load_file_to_lines(file_path)
# Purpose:    Assigns file path to global_file variable
#             and
#             loads contents of the file(lines) as list to global_lines
# =============================================================================
def load_file_to_lines(file_path):
    global global_lines
    global global_file
    global_file = file_path
    with open(file_path) as f:
        global_lines = f.read().splitlines()
# *****************************************************************************
# =============================================================================
# Name:       empty_lines()
# Purpose:    Cleares values from global_lines and global_file to be reassigned
# =============================================================================
def empty_lines():
    global global_lines
    global global_file
    global_lines = ""
    global_file = ""

# *****************************************************************************
# =============================================================================
# Name:       find_regex()
# Purpose:    Checks a file for regex in different lists
#             Abandoned and not tested fully. Might not be working
# =============================================================================
def find_regex():
    # TODO regex to find:
    # email                             email = re.findall(r'[\w.-]+@[\w.-]+.\w+', string_ip)
    # website (www)                     www = re.findall('www.+(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', string_ip)
    # website (http[s])                 urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', string_ip)
    # ip                                ip = re.findall(r'[0-9]+(?:\.[0-9]+){3}', string_ip)
    # base64 (known to exist)           test = re.compile(r'(?:[A-Za-z0-9+/]{4}){2,}(?:[A-Za-z0-9+/]{2}[AEIMQUYcgkosw048]=|[A-Za-z0-9+/][AQgw]==)')

    regex_dict = dict()
    regex_dict["reg_email"] = r'[\w.-]+@[\w.-]+.\w+'
    regex_dict["reg_web_www"] = 'www.+(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    regex_dict["reg_web_http"] = 'https?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    regex_dict["reg_ip"] = r'[0-9]+(?:\.[0-9]+){3}'
    regex_dict["reg_base64"] = r'(?:[A-Za-z0-9+/]{4}){2,}(?:[A-Za-z0-9+/]{2}[AEIMQUYcgkosw048]=|[A-Za-z0-9+/][AQgw]==)'

    regex_list = [regex_dict["reg_email"], regex_dict["reg_web_www"], regex_dict["reg_web_http"], regex_dict["reg_ip"], regex_dict["reg_base64"]]
    tmp_output = []
    tmp_content = []
    for word_item in regex_list:
        tmp_count = 0
        word_label = False
        for line in global_lines:
            tmp_count += 1
            if re.findall(word_item, line.lower()) and "jd-core version" not in line.lower():
                if not word_label:
                    tmp_content.append("----------------------------------------------------------------")
                    tmp_content.append("Word :" + regex_dict.keys()[regex_dict.values().index(word_item)])
                    tmp_content.append("----------------------------------------------------------------")
                    word_label = True
                tmp_content.append((str(tmp_count)) + "   :" + line)
    if tmp_content:
        tmp_output.append("===========================================================================================")
        tmp_output.append("Filename :" + global_file)
        tmp_output.append("============================================================================================")
        tmp_output.extend(tmp_content)
        tmp_output.append("")
        tmp_output.append("")
        tmp_output.append("")
        tmp_output.append("")
    for line_entry in tmp_output:
        print (line_entry)
    empty_lines()
# *****************************************************************************
# =============================================================================
# Name:       find_word_in_list()
# Purpose:    Checks a file for key words in different lists
#             prints out file name, line number and contents of the line if
#             line contained key word.
# =============================================================================
def find_word_in_list():
    tmp_authentication = ["user", "username", "usr", "pass", "pwd", "password", "login"]
    tmp_network = ["port", "http", "https", "udp", "tcp", "ftp", "smtp", "telnet", "service", "protocol"]
    tmp_hashing = ["hash", "salt", "sha", "md5", "encrypt"]
    tmp_company = ["mybabyok", "foscam", "seecamera", "cameraftp", "hti", "ne01","ne-01"]
    tmp_all_lists = [tmp_authentication,tmp_network,tmp_hashing,tmp_company]

    banned_list = ["package android", "qualified name", "import"]
    tmp_output = []
    tmp_content = []

    for word_list in tmp_all_lists:
        for word_item in word_list:
            tmp_count = 0
            word_label = False
            for line in global_lines:
                tmp_count += 1
                if any(ban_item in line.lower() for ban_item in banned_list):
                    pass
                else:
                    if word_item in line.lower():

                        if not word_label:
                            tmp_content.append('Searched Criteria: '+str(word_list))
                            tmp_content.append("----------------------------------------------------------------")
                            tmp_content.append("Word :" + word_item)
                            tmp_content.append("----------------------------------------------------------------")
                            word_label = True
                        tmp_content.append((str(tmp_count)) + "   :" + line)
            if tmp_content:
                tmp_output.append("===========================================================================================")
                tmp_output.append("Filename :" + global_file)
                tmp_output.append("============================================================================================")
                tmp_output.extend(tmp_content)
                tmp_output.append("")
                tmp_output.append("")
                tmp_output.append("")
                tmp_output.append("")
    for line_entry in tmp_output:
        print (line_entry)
    empty_lines()

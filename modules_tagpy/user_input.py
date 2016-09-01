import argparse

# =============================================================================
# Name:       validate_path(path_string)
# Arguments:  path_string = string input from the user
# Purpose:    Returns a input value or raises Error
# =============================================================================
def validate_path(path_string):
    import os
    mod_path_string = os.path.join(path_string, '')
    if os.path.isdir(mod_path_string):
        # print(mod_path_string)
        return mod_path_string             # add trailing slash to path if missing at end
    else:
        raise argparse.ArgumentTypeError("%s is not a valid directory" % mod_path_string)  # not directory or file


parser = argparse.ArgumentParser()
parser.add_argument("target", metavar='directory', type=validate_path,
                         help="""
                              -----------------------------------------------------------
                              'tagpy.py directory' - search files in directory
                               -----------------------------------------------------------
                         """)

args = parser.parse_args()



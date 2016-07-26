class UserInput:

    # =============================================================================
    # Name:       __init__(self, input_path)
    # Purpose:    Initialises variables for _input_path and _list_of_files
    # =============================================================================
    def __init__(self, settings):
        import argparse
        self._st = settings
        self.parser = argparse.ArgumentParser()
        self.set_up_parser()
        self._recursive = False                             # value gets changed from inside the file path check
        self.args = self.parser.parse_args()
        self._st.set_verbose(self.update_if_not_none(self._st.get_verbose(), self.args.verbose))
        self._st.set_target(self.update_if_not_none(self._st.get_target(), self.args.target))
        self._st.set_recursive(self.update_if_not_none(self._st.get_recursive(), self._recursive))


    # =============================================================================
    # *****************************************************************************
    # =============================================================================
    # Name:       set_up_parser
    # Purpose:    Sets up all settings for argparse parser
    # =============================================================================
    def set_up_parser(self):

        # =============================================================================
        # Argument Name:    target - positional argument
        # Argument Type:    argument value
        # Functionality:    Receives target file or directory or recursive directory.
        # =============================================================================
        self.parser.add_argument("target", metavar='file', type=self.validate_path_to_hash, # TODO Add multiple arguments and make sure all get listed
                            help="""
                            -----------------------------------------------------
                            Target IP address to be scanned. Use examples below:
                            'hashpy.py file.txt'      - hash single file to hash
                            'hashpy.py directory'     - hash files in directory
                            'hashpy.py directory -r'  - hash all files recursively
                            -----------------------------------------------------
                            """)
        # =============================================================================
        # Argument Name:    -v
        # Argument Type:    flag
        # Functionality:    Toggles ON verbose mode for output to console. TODO IMPLEMENT
        # =============================================================================
        self.parser.add_argument("-v", "--verbose", action='store_true',
                            help="""
                            -----------------------------------------------------
                            Displays results of the hashing in console after hashing
                            is completed.
                            -----------------------------------------------------
                            """)
    # =============================================================================
    # *****************************************************************************
    # =============================================================================
    # Name:       update_if_not_None(org_value,new_value)
    # Arguments:  org_value = a 'default' value
    # Arguments:  new_value = user's override to default value
    # Purpose:    Returns a value for the setting
    # =============================================================================
    @staticmethod
    def update_if_not_none(org_value, new_value):
        if new_value is None:
            return org_value
        else:
            return new_value

    # =============================================================================
    # Name:       validate_path_to_hash(path_string)
    # Arguments:  path_string = string input from the user to hash
    # Purpose:    Returns a input value or raises Error
    # =============================================================================
    def validate_path_to_hash(self, path_string):
        import os
        tmp_recursive = False
        # find out if it's recursive or not or file
        if path_string.endswith("*"):                           # if last character is * for all recursively
            temp_path = (path_string[:len(path_string)-1])
            tmp_recursive = True
        else:
            temp_path = path_string                             # no changes to path at this stage

        if os.path.isfile(temp_path):
            pass                                                # no need to update anything as temp_path is valid file
        elif os.path.isdir(temp_path):
            temp_path = os.path.join(temp_path, '')             # add trailing slash to path if missing at end
        else:
            raise self.argparse.ArgumentTypeError("%s is not a invalid file or directory" % temp_path)   # not directory or file
        self._recursive = tmp_recursive
        return temp_path                                        # returns modified path

    # =============================================================================
    # *****************************************************************************
    # =============================================================================
    # Name:       validate_path_to_save(path_string)
    # Arguments:  path_string = string input from the user to hash
    # Purpose:    Returns a input value or raises Error
    # =============================================================================
    def validate_path_to_save(self, path_string):
        import os
        import sys

        directory_name = os.path.dirname(path_string)
        # extracts directory name from path with or without file
        file_name = os.path.basename(path_string)

        # minor fixes to path string if missing parts
        if not directory_name and not file_name:
            # if directory name and filename is not given
            raise self.argparse.ArgumentTypeError("No Filename for the file or full Path to file location was specified.")
        elif not directory_name and file_name:
            # if directory name is not specified but file name is, assume that save location is script location
            directory_name = os.path.dirname(os.path.realpath(sys.argv[0]))  # extracts directory from abs path of script
            # assign new path_string
            path_string = os.path.join(directory_name, file_name)
        elif directory_name and not file_name:
            # if directory name but no filename is not given
            raise self.argparse.ArgumentTypeError("No Filename for the file was specified.")
        else:
            # Seems fine I guess so it proceeds
            pass

        if os.path.isfile(path_string) and ("-ow" in sys.argv):
            # TODO CHECKING IF -ow is in sys.argv is a dirty hack because Cannot check if -ow is true from argparse
            # if file already exists in the path and name, but overwrite is True - return string
            return path_string
        elif os.path.isfile(path_string) and not ("-ow" in sys.argv):
            # TODO CHECKING IF -ow is in sys.argv is a dirty hack because Cannot check if -ow is true from argparse
            # if file already exists in the path and name, but overwrite is False - Error
            raise self.argparse.ArgumentTypeError("%s already exists, "
                                             "Overwrite is not enabled. "
                                             "Use -ow flag to enable overwrite." % path_string)

        elif os.path.isdir(directory_name) and not os.path.isfile(file_name):
            # if directory exists but the file does not yet exist - return string
            return path_string
        else:
            # not a valid directory or does not exist
            raise self.argparse.ArgumentTypeError("%s is not a valid directory." % directory_name)


    # =============================================================================
    # *****************************************************************************
    # =============================================================================
    # Name:       validate_hash_type(hash_type)
    # Arguments:  hash_type = a string representing type of hash to be used
    # Purpose:    Returns a hash type or raises error
    # =============================================================================
    def validate_hash_type(self, hash_type):
        possible_hashes = ["MD5", "SHA1", "SHA224", "SHA256", "SHA84", "SHA512"]
        hash_type = hash_type.upper()           # converts characters to upper case to match list

        if hash_type in possible_hashes:
            return hash_type
        else:
            raise self.argparse.ArgumentTypeError("%s is not a valid type of hash." % hash_type)

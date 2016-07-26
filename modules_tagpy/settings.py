class Settings:
    # =============================================================================
    # Name:       __init__(self, input_path)
    # Purpose:    Initialises variables for _input_path and _list_of_files
    # =============================================================================
    def __init__(self):
        import time
        import collections
        self._start_time = time.time()
        self._settings_dict = collections.OrderedDict()
        self._settings_dict['Target'] = None
        self._settings_dict['Recursive'] = False
        self._settings_dict['Verbose'] = False

    # =============================================================================
    # GETTERS FOR SETTINGS
    # Purpose:      Return values that are supposed to be protected _ and not modified
    #               outside this module.
    # =============================================================================
    def get_time(self):
        return self._start_time

    def get_target(self):
        return self._settings_dict['Target']

    def set_target(self, value):
        self._settings_dict['Target'] = value


    def get_recursive(self):
        return self._settings_dict['Recursive']

    def set_recursive(self, value):
        self._settings_dict['Recursive'] = value


    def get_verbose(self):
        return self._settings_dict['Verbose']

    def set_verbose(self, value):
        self._settings_dict['Verbose'] = value

    def print_settings(self):
        print ("")
        print ("{:<15}{:<10}".format('Setting', 'Value'))
        for option, value in self._settings_dict.iteritems():
            print ("{:<15}{:<10}".format(str(option), str(value)))

class FileDiscovery:
    # =============================================================================
    # Name:       __init__(self, input_path)
    # Purpose:    Initialises variables for _input_path and _list_of_files
    # =============================================================================
    def __init__(self, settings):
        self._input_path = settings.get_target()
        self._list_of_files = []
        self._recursive_search = settings.get_recursive()
        self._verbose = settings.get_verbose()

    # =============================================================================
    # Name:       run_discovered_files(self)
    # Purpose:    Runs discovery for path specified
    # =============================================================================
    def run_file_discovery(self):
        self._discover_files()

    # =============================================================================
    # Name:       generate_list_of_files(self)
    # Purpose:    Generates a list of all directories and paths for files
    # =============================================================================
    def _discover_files(self):
        import os
        if os.path.isfile(self._input_path):
            self._generate_single_file_list()
        elif os.path.isdir(self._input_path): # is directory
            if self._recursive_search:
                self._generate_recursive_file_list()       # recursive directory
            else:
                self._generate_directory_file_list()       # single directory

    # =============================================================================
    # Name:       generate_recursive_file_list(self)
    # Purpose:    Returns a list of strings that represent paths where files were found with file names
    # =============================================================================
    def _generate_recursive_file_list(self):
        import os
        for dir_path, directories, files in os.walk(self._input_path):
            for file_name in files:
                full_path = (os.path.join(dir_path, file_name))
                if self._verbose:
                    self._get_discovery_status()
                self._list_of_files.append(full_path)# appends directly to list

    # =============================================================================
    # Name:       generate_directory_file_list(self)
    # Purpose:    Returns a list of strings that represent paths where files were found with file names within directory
    # =============================================================================
    def _generate_directory_file_list(self):
        import os
        path_triple = (next(os.walk(self._input_path)))
        # generates triple with [path, directories and files]
        dir_path = path_triple[0]
        top_files = path_triple[2]
        for file_name in top_files:
            full_path = (os.path.join(dir_path, file_name))
            if self._verbose:
                self._get_discovery_status()
            self._list_of_files.append(full_path)                   # appends directly to list

    # =============================================================================
    # Name:       generate_single_file_list(self)
    # Purpose:    Returns a string for file path in a list format
    # =============================================================================
    def _generate_single_file_list(self):
        if self._verbose:
            self._get_discovery_status()
        self._list_of_files.append(self._input_path)

    # =============================================================================
    # Name:       get_discovery_status(file_count)
    # Purpose:    Displays formatted console output showing number of files discovered.
    # =============================================================================
    def _get_discovery_status(self):
        import sys
        text = "\r{0}: {1} {2}".format("Discovered", (len(self._list_of_files) + 1), "files to hash.")
        sys.stderr.write(text)

    # =============================================================================
    # Name:       get_list_of_files(self)
    # Purpose:    Returns a combined list of all directories and paths for files
    # =============================================================================
    def get_discovered_files(self):
        return self._list_of_files

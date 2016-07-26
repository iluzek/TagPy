
import modules_tagpy.settings
import modules_tagpy.user_input
import modules_tagpy.file_discovery
import modules_tagpy.file_loader as load_file


def run_app():
    st = modules_tagpy.settings.Settings()          #takes in directory. Trim rest?
    modules_tagpy.user_input.UserInput(st)         # initializes user input

    discovery = modules_tagpy.file_discovery.FileDiscovery(st)      #initilies file discovery
    discovery.run_file_discovery()  #runs discovery
    discovered_files = discovery.get_discovered_files() #list of discovered files

    files_counter = 0
    for file_from_list in discovered_files:
        files_counter += 1
        load_file.load_file_to_lines(file_from_list)
        load_file.find_word_in_list()
        load_file.empty_lines()
    print ("Files scanned: " + str(files_counter))

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

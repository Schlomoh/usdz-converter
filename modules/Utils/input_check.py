import glob

from modules.Utils.directory_check import directory_check
from modules.Utils.Error_handling import Error_handling

def input_check(
                input_selection,
                extensions
                ):     
    Err = Error_handling()
    found = False
    input_list = []

    #check if input selection is a path or file ending with specified extension

    s = len(input_selection) - 4
    stop = len(input_selection) - 6

    while s >= stop:
        extesion_test = input_selection[s: len(input_selection)]
        for extension in extensions:
            if extesion_test == extension:
                input_list.append(input_selection)
                found = True
                print('Single file input: ' + str(found), chr(10))
                return input_list
        s -= 1
            
    if not found:         
        selection = directory_check(input_selection)
        glob_list = []
        for extension in extensions:
            glob_pattern = selection + '**/*' + extension
            if glob.glob(glob_pattern) != []:
                glob_list = glob.glob(glob_pattern, recursive=True)
    
        if glob_list == []:
            for extension in extensions:
                glob_pattern = selection + '*/**/*' + extension
                if glob.glob(glob_pattern) != []:
                    glob_list = glob.glob(glob_pattern, recursive=True)
                
        if glob_list != []:
            return glob_list

        else: 
            Err.no_input()
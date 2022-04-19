import glob
from modules.Utils.Error_handling import Error_handling


def directory_check(directory):

    end = len(directory) - 1 
    if directory[end] != '/':
        directory = directory  + '/'
    return directory

def input_check(input_selection):     
    
    Err = Error_handling()
    found = False
    input_list = []
    extensions = ['.zip', '.glb', '.gltf', '.usdz', '.fbx', '.obj']

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



def output_check(output_selection):
    return directory_check(output_selection)
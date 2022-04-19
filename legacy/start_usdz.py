import os
import glob

from controller import Controller

def input_select(selection):
    extensions = ['.glb', '.gltf', '.usdz', '.fbx']
    glob_list = []

    for extension in extensions:
        glob_pattern = selection + '**/*' + extension
        if glob.glob(glob_pattern) != []:
            glob_list = glob.glob(glob_pattern, recursive=True)
    
    if glob_list == []:
        print('1st empty')
        for extension in extensions:
            glob_pattern = selection + '*/**/*' + extension
            if glob.glob(glob_pattern) != []:
                glob_list = glob.glob(glob_pattern, recursive=True)
            
    if glob_list != []:
        return glob_list
    else: 
        print('The input is empty')

def start():
    
    method = 'e'

    conversion = 'gltf-usdz'

    input_selection = []
    input_path = os.path.abspath('./_in/')

    input_selection = input_select(input_path)
    print('Input selection: ', input_selection)

    output_selection = str(os.path.abspath('./_out/') + '/')

    print('Output selection: ', output_selection)

    texture_resizing = 100
    
    texture_quality = 100

    conversion = Controller(
                            method, 
                            conversion, 
                            input_selection,
                            output_selection,
                            texture_resizing,
                            texture_quality
    )

    conversion.start()

start()
import sys
import zlib
import glob

from modules.Utils.selection_check import input_check, output_check
from modules.Utils.texture_resize import texture_resizing
from modules.Utils.docker_initiation import docker_initiation

class Util:
   
    def __init__(self, arguments):

        self.arguments = arguments

    def selection_check(self, input, output):
        selections = {}
        selections['input'] = input_check(input)
        selections['output'] = output_check(output)
        return selections



    def get_conversion_selection(self, file, output_format):
        extensions = ['.zip', '.glb', '.gltf', '.usdz', '.fbx', '.obj']

        start = len(file) - 5
        while start < len(file):
            for extension in extensions:
                if extension == file[start:len(file)]:
                    selection = extension[1:len(extension)] 
                    conversion_selection = selection + '-' + output_format
                    print('Selected conversion: ', conversion_selection, chr(10))
                    return conversion_selection
            start += 1

    
    def split_file_name(self, file):

        found = False
        i = len(file) - 1
            
        while i >= 0:
            if file[i] == '/':
                file_name = file[i + 1: len(file)]
                file_path = file[0: i + 1]
                found = True
                break
            i -= 1

        if not found:
            file_path = './'
            file_name = file

        split = {
            'file_path' : file_path,
            'file_name' : file_name
        }
        print('The input selection was split into ' + file_path + ' and ' + file_name, chr(10))

        return split


    def docker_initiation(self):
        pass


    def texture_method(self, texture_resizing_value, texture_quality, file_path, temp_directory):
        texture_resizing(
                        texture_resizing_value,
                        texture_quality,
                        file_path,
                        temp_directory,
                        )


    def zip_util(self, input):
        pass        
import fnmatch
import os
import sys
import time
import glob
import tempfile

from shutil import copy2
from PIL import Image as Pil_image

sys.path.append('.')

from exporter import Docker_export_convert
from exporter import Gltf_to_glb
#import importer

class Error_handler:

    def __init__(self):
        pass



class Controller(Error_handler):

    def __init__(
                self,
                method,
                conversion,
                input_selection,
                output_selection,
                texture_resizing,
                texture_quality
                ):
        
        self.method = method
        self.input_selection = input_selection
        self.output_selection = output_selection
        self.conversion = conversion
        self.texture_downsizing = texture_resizing
        self.texture_quality = texture_quality

        #   conversion
        #   'gltf-glb'
        #   'gltf-usdz'
        #   'glb-gltf'


    def split_filename(self, file):
        
        found = False
        i = len(file) - 1
        
        while i >= 0:
            if file[i] == '/':
                self.file_name = file[i + 1: len(file)]
                self.file_path = file[0: i + 1]
                found = True
                break

            elif file[i] == '\\':
                self.file_name = file[i + 1: len(file)]
                self.file_path = file[0: i + 1]
                found = True
                break
            i -= 1

        if not found:
            self.file_path = './'
            self.file_name = file

        print(
            'The input selection was split into ',
            self.file_path,
            ' and ',
            self.file_name,
            chr(10)
            )


    def texture_resize(self, temp_directory):
        
        file_path = self.file_path
        texture_quality = int(self.texture_quality)
        texture_downsizing = int(self.texture_downsizing)

        image_texture_files = ['*.png', '*.jpg']
        gltf_files = ['*.bin', '*.gltf']
        counter = 1
        
        print('Image texture quality is set to: ' + str(texture_quality) + '%', chr(10))
        decimal_resize_amount = texture_downsizing / 100
        print('Resizing textures down by: ' + str(texture_downsizing) + '%', chr(10))

        if texture_downsizing != 100 or texture_quality != 100:
            for file_type in gltf_files:
                for gltf_file in os.listdir(file_path):
                    if fnmatch.fnmatch(gltf_file, file_type):
                        full_gltf_file = file_path + gltf_file
                        copy2(full_gltf_file, temp_directory)
                        print('Copied ' + gltf_file + ' into temporary location', chr(10))

            for image_type in image_texture_files:
                for file in os.listdir(file_path):
                    if fnmatch.fnmatch(file, image_type):
                        full_texture_file = file_path + file
                        print('Resizing texture #' + str(counter) + ': ' + full_texture_file)

                        texture = Pil_image.open(full_texture_file)

                        save = temp_directory + file

                        new_texture_height = int(texture.height * decimal_resize_amount)
                        new_texture_width = int(texture.width * decimal_resize_amount)
                        
                        print('New image dimensions: ',
                              str(new_texture_height) + 'x' + str(new_texture_width), chr(10))

                        resized_texture = texture.resize((new_texture_width, new_texture_height))
                            
                        resized_texture.save(save, quality = texture_quality)
                            
                        counter += 1                
                
    def fimport(self):
        pass


    def fexport(self, count, file_path):

        output_selection = self.output_selection
        file_name = self.file_name
        print('USDZ conversion initiated...', chr(10))
        
        if self.conversion == 'gltf-usdz':
            selection = 'usdz'
            converter = Docker_export_convert(
                                            file_name,
                                            file_path,
                                            output_selection,
                                            selection,
                                            count
                                            )
            print('USDZ initiation complete!', chr(10))
            converter.convert_to_usdz()
        
        elif self.conversion == 'gltf-glb':
            selection = 'glb'
            converter = Gltf_to_glb(
                                    file_name,
                                    file_path,
                                    output_selection,
                                    selection,
                                    count
                                    )
            converter.gl_converter()
        
        else:
            print('NO CONVERSION SET ... FUCKIN IDIOT')


    def start(self):

        input_selection = self.input_selection
        method = self.method
        texture_downsizing = self.texture_downsizing
#       output_selection = self.output_selection
#       draco_compression = self.draco_compression
#       texture_downsizing = self.texture_downsizing
        
        #start time keeping 
        start_time = time.time()

        if method == 'i':       #import call
            self.fimport()

        elif method == 'e':     #export call
            print('Export call succesful', chr(10))
            count = 1

            for file in input_selection:
                print('Input selection #' + str(count) + ': ' + file)

                self.split_filename(file)

                if texture_downsizing != 100:
                    with tempfile.TemporaryDirectory() as temp_directory:
                        temp_directory = temp_directory + '/'
                        self.texture_resize(temp_directory)
                        print('### Texture resize complete ###', chr(10))
                        
                        print('### Starting export ###', chr(10))
                        self.fexport(count, temp_directory)
                else:
                    self.fexport(count, self.file_path)
                count += 1
        else:
            print('no method selected')

        print(
            'The conversion script completed in ',
            round((time.time() - start_time),2),
            'seconds.',
            chr(10)
            )



#only necessary for cli execution
def arugment_handling():

    sys_args = sys.argv
    i = 0 
    input_selection = []

    for Param in sys_args:
        
        i += 1

        if Param == '-i':     
            input_argument = sys_args[i]
            extensions = ['.glb', '.gltf', '.usdz', '.fbx']
            found = False

            s = len(input_argument) - 4
            stop = len(input_argument) - 6

            #check if input selection is a path or file ending with specified extension
            while s >= stop:
                extesion_test = input_argument[s: len(input_argument)]
                for extension in extensions:
                    if extesion_test == extension:
                        input_selection.append(input_argument)
                        found = True
                        print('found: ', str(found))
                        break
                s -= 1
            
            if not found:         
                end = len(input_argument) - 1 
                if input_argument[end] != '/':
                    input_argument = input_argument  + '/'           
                glob_list = []
                for extension in extensions:
                    glob_pattern = input_argument + '**/*' + extension
                    if glob.glob(glob_pattern) != []:
                        glob_list = glob.glob(glob_pattern, recursive=True)
                
                if glob_list != []:
                    for path in glob_list:
                        input_selection.append(path)
                else: 
                    print('no input')
                    print('EXITING')
                    exit()

        elif Param == '-o':      
            output_argument = sys_args[i] 
            end = len(output_argument) - 1 
            for chr in output_argument:
                if chr == '\\':
                    if output_argument[end] != '\\':
                        output_argument = output_argument  + '\\'
                        break
                if chr == '/':
                    if output_argument[end] != '/':
                        output_argument = output_argument  + '/'
                        break

            output_selection = output_argument
            
        elif Param == '-d': 
            texture_resizing = sys_args[i] 

        elif Param == '-q':
            texture_quality = sys_args[i]

        elif Param == '-m':
            method = sys_args[i]

        elif Param == '-c':
            conversion_argument = sys_args[i]
            if not conversion_argument:
                print('no conversion set.')
                print('EXITING')
                exit()
            else:
                conversion = conversion_argument 

    print('Input Selection: ' + str(input_selection))
    print('Output directory: ' + output_selection, chr(10))
    
    controller = Controller(
                            method,
                            conversion,
                            input_selection,
                            output_selection,
                            texture_resizing,
                            texture_quality
                            )
    controller.start()

    
#   required functionality:
#   timekeeping
#   errorhandling
#   recursive opening of folders 
#   batch processing of files
#   cli argument handling
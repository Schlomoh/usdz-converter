import sys
import os


from modules.Conversion.gltf_gltf import gltf_gltf
from modules.Conversion.gltf_glb import gltf_glb
from modules.Conversion.gltf_usdz import gltf_usdz
from modules.Conversion.glb_gltf import glb_gltf
from modules.Conversion.usdz_gltf import usdz_gltf
from modules.Conversion.fbx_gltf import fbx_gltf
from modules.Conversion.obj_gltf import obj_gltf


from modules.Util import Util


class Convert:
    
    def __init__(self, arguments):


#   create dict with arguments from parameters
        self.arguments = arguments
    
    def convert(self, arguments, conversion_selection):

        if conversion_selection == 'gltf-gltf':
            gltf_gltf(arguments)
        elif conversion_selection == 'glb-gltf':
            glb_gltf(arguments)
        elif conversion_selection == 'gltf-glb':
            gltf_glb(arguments)
        elif conversion_selection == 'gltf-usdz':
            gltf_usdz(arguments)
        elif conversion_selection == 'fbx-gltf':
            pass
        elif conversion_selection == 'obj-gltf':
            pass
        elif conversion_selection == 'dae-gltf':
            pass


    def start(
            self,
            single_input,
            temp_directory,
            count
            ):
        
        
        arguments = self.arguments

#   local variables from arguments dict
        input_selection = arguments['input_selection']
        output_format = arguments['output_format']
        texture_resizing = arguments['texture_resizing']
        resizing_amount = arguments['resizing_amount']
        texture_quality = arguments['texture_quality']

#   input selection split
        Utility = Util(input_selection)
        split_file_name = Utility.split_file_name(single_input)

#   adding seperate file path and name to arguments dict
        arguments['file_path'] = split_file_name['file_path']
        arguments['file_name'] = split_file_name['file_name']
        arguments['count'] = count

#   getting local variabble from dict        
        file_path = arguments['file_path']
        file_name = arguments['file_name']


#   checks if texture resizing is active and uses temp dir accordingly
        if texture_resizing:
            print('Using temp directory for image resizing')
            print('Starting texture resize...', chr(10))

#   alters textures and saves into temp directory            
            input_directory = temp_directory
            
            Utility.texture_method(
                                resizing_amount,
                                texture_quality,
                                file_path,
                                input_directory
                                )

#   if texture resizing is not activated use default path for file import
#   resizing method does not get called
        else:
            print('Starting default conversion without texture resizing...', chr(10))
            input_directory = file_path


#   adds input directory to arguments dict depending on active texture resizing
        arguments['input_directory'] = input_directory

#   creates token to select correct conversion method
        conversion_selection = Utility.get_conversion_selection(file_name, output_format)

#   calls convert function
        self.convert(arguments, conversion_selection)
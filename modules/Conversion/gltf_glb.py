from pygltflib import GLTF2, BufferFormat
from pygltflib.utils import Image, ImageFormat

import os
import fnmatch

def buffer_conversion(transfer_file, inp_path):

    #patterns for file import
    png_pattern = '*.png'
    jpg_pattern = '*.jpg'

    image = Image()

    for file in os.listdir(inp_path):
        if fnmatch.fnmatch(file, png_pattern) or fnmatch.fnmatch(file, jpg_pattern):
            image.uri = file
            transfer_file.images.append(image)
        
    transfer_file.convert_images(ImageFormat.DATAURI)
    transfer_file.convert_buffers(BufferFormat.BINARYBLOB)

    return transfer_file
    

def gltf_glb(arguments):

    input_path = arguments['file_path']
    input_file = arguments['file_name']
    output_path = arguments['output_path']
    output_name_pattern = arguments['output_name']
    count = arguments['count']


    #sets the output file name 
    output_extension = '.glb'
    output_name_cut = len(input_file) - len(output_extension)
    
    if output_name_pattern != None:
        output_name = output_name_pattern + '-' + str(count) + output_extension
    else:
        output_name = input_file[0:output_name_cut] + '_#' + str(count) + output_extension

    #sets output as outputpath + output file name
    save =  output_path + output_name

### actual file conversion ###

    #import file
    import_file = GLTF2().load(input_path + input_file)
        
    #convert glff textures to binary format
    import_file = buffer_conversion(import_file, input_path)

    #save converted file
    import_file.save(save)
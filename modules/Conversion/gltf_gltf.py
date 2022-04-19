from shutil import copy2
import os
import fnmatch

def gltf_gltf(arguments):

#   declaring the local variables from arguments dict
    file_path = arguments['file_path']
    output_path = arguments['output_path']

    gltf_extensions = ['.gltf', '.bin']

#   copying the .gltf and .bin file to output directory
    for file_type in gltf_extensions:
        for gltf_file in os.listdir(file_path):
            if fnmatch.fnmatch(gltf_file, file_type):
                full_gltf_file = file_path + gltf_file
                copy2(full_gltf_file, output_path)
                print('Copied ' + gltf_file + ' into output location', chr(10))

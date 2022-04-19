#   only actual conversion here
#   controller recognizes the selected method


import docker
from pygltflib import GLTF2, BufferFormat
from pygltflib.utils import Image, ImageFormat
import fnmatch, os


class Initiation:

    def __init__(self, inp_filename, inp_path, out_path, selection, count):
        
        self.inp_filename = inp_filename
        self.inp_path = inp_path
        self.out_path = out_path
        self.selection = selection
        self.count = count

class Docker_export_convert(Initiation):

#   class for converting to usd or usdz
   
#   pip install docker

    def __init__(self, inp_filename, inp_path, out_path, selection, count):
        
        super().__init__(inp_filename, inp_path, out_path, selection, count)
        self.client = docker.from_env()

    def remove_backslash(self, input):

        stack = ''
        i = 0
        found = False

        while i < len(input) -1:
            if input[i] == "\\":
                stack = stack + input[0:i] + '/'
                input = input[i+1: len(input)]
                found = True
            i += 1
            if found:
                found = False
                i = 0
        stack = stack + input
        end = len(input) -1
        if input[end] == '\\':
            input = input[0:end] + '/'
        return stack

    def convert_to_usdz(self):
       
        print('Converter started')
        selection = self.selection
        input_file = self.inp_filename
        input_path = self.inp_path
        output_path = self.out_path
        client = self.client
        count = self.count
        
        for chr in input_path:
            if chr == '\\':
                self.remove_backslash(input_path)
                break 
        for chr in output_path:
            if chr == '\\':
                self.remove_backslash(output_path)
                break

        #setting the command
        output_extension = '.' + selection
        output_name_cut = len(input_file) - (len(selection) + 1)
        output_name = input_file[0:output_name_cut] + '_conv_' + str(count) + output_extension

        docker_in_path = '/usr/src/app/_in/'
        docker_out_path = '/usr/src/app/_out/'

        input_argument = docker_in_path + input_file
        output_argument = docker_out_path + output_name
        
        #docker command to mount specified volume
        docker_vol_par = {input_path:{'bind':docker_in_path, 'mode':'rw'}, 
                          output_path:{'bind':docker_out_path, 'mode':'rw'}}

        print('input argument: ' + input_argument)
        print('output argument: ' + output_argument )
        
        tool = 'usd_from_gltf '
        command = tool + input_argument + ' ' + output_argument
        
        print('docker volume binding: ', docker_vol_par)
        print('docker command: ', command)

        #run the defined conversion command in the docker container
        client.containers.run('conv-tools:latest', command, remove = True, volumes = docker_vol_par)
        print('Docker conversion completed!')



class Gltf_to_glb(Initiation):

#   classs for converting from gltf to glb (binary)

#   pip install pygltflib

    def __init__(self, inp_filename, inp_path, out_path, selection, count):
        super().__init__(inp_filename, inp_path, out_path, selection, count)


    def buffer_conversion(self, transfer_file):

        #patterns for file import
        png_pattern = '*.png'
        jpg_pattern = '*.jpg'

        image = Image()

        for file in os.listdir(self.inp_path):
            if fnmatch.fnmatch(file, png_pattern) or fnmatch.fnmatch(file, jpg_pattern):
                image.uri = file
                transfer_file.images.append(image)
        
        transfer_file.convert_images(ImageFormat.DATAURI)
        transfer_file.convert_buffers(BufferFormat.BINARYBLOB)

        return transfer_file


    def gl_converter(self):

        #local variable declaration
        input_path = self.inp_path
        input_file = self.inp_filename
        count = self.count
        select = self.selection
        out_path = self.out_path

        #sets the output file name 
        output_extension = '.' + select
        output_name_cut = len(input_file) - len(output_extension)
        output_name = input_file[0:output_name_cut] + '_conv_' + str(count) + output_extension

        #sets output as outputpath + output file name
        save =  out_path + output_name

    ### actual file conversion ###

        #import file
        import_file = GLTF2().load(input_path + input_file)
        
        #convert glff textures to binary format
        import_file = self.buffer_conversion(import_file)

        #save converted file
        import_file.save(save)
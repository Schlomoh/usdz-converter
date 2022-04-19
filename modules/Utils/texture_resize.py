import os
import sys
import fnmatch
from shutil import copy2


#importing Python image library
from PIL import Image as Pil_image

#   resizes image texture of gltf files and copies
#   .gltf and .bin file to temp directory

def texture_resizing(texture_resize, texture_quality, file_path, temp_directory):

        texture_resize = int(texture_resize)
        texture_quality = int(texture_quality)

        texture_extensions = ['*.png', '*.jpg']
        gltf_extensions = ['*.bin', '*.gltf']
        counter = 1
        
        print('Image texture quality is set to: ' + str(texture_quality) + '%', chr(10))
        decimal_resize_amount = texture_resize / 100
        print('Resizing textures down by: ' + str(texture_resize) + '%', chr(10))


#   copying the gltf and bin file to temp directory
        for file_type in gltf_extensions:
            for gltf_file in os.listdir(file_path):
                if fnmatch.fnmatch(gltf_file, file_type):
                    full_gltf_file = file_path + gltf_file
                    copy2(full_gltf_file, temp_directory)
                    print('Copied ' + gltf_file + ' into temporary location', chr(10))

#   resizing the actual textures and saving them to temp directory
        for image_type in texture_extensions:
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
                
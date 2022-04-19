from pygltflib import GLTF2, BufferFormat
from pygltflib.utils import Image, ImageFormat


def glb_gltf(arguments):

    file_name = arguments['file_name']
    file_path = arguments['file_path']
    output_path = arguments['output_path']
    output_pattern = arguments['output_name']
    count = arguments['count']



    output_extension = '.gltf'
    output_name_cut = len(file_name) - len(output_extension) + 1
    
    if output_pattern:
        output_name = output_pattern + '-' + str(count)
    else:
        output_name = file_name[0:output_name_cut]

    output_file = output_name + '_#' + str(count) + output_extension

    full_file_name = file_path + file_name

    import_file = GLTF2().load(full_file_name)    
    
    i = 0
    for im in import_file.images:
        #print('before: ' + str(im))
        if im.mimeType == 'image/jpeg':
            image_type = '.jpg'
            print('found jpeg...')
            print(import_file.images[i].name)
            import_file.images[i].name = output_name + '_' + str(i+1) + image_type
            print(import_file.images[i].name)   
        #  print('after: ' + str(im))

        if im.mimeType == 'image/png':
            image_type = '.png'
            print(import_file.images[i].name)
            import_file.images[i].name = output_name + '_' + str(i+1) + image_type
            print(import_file.images[i].name)
            print('found png...')
        #    print('after: ' + str(im))

        i += 1
    
    print('Reading image files out of binary buffer', chr(10))

    save =  output_path + output_file
    
    import_file.convert_images(ImageFormat.FILE)
    import_file.save(save)

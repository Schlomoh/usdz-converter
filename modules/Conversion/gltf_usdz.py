import docker


def gltf_usdz(arguments):

    input_path = arguments['file_path']
    input_file = arguments['file_name']
    output_path = arguments['output_path']
    count = arguments['count']

    client = docker.from_env()
        
    #setting the command
    output_extension = '.usdz'
    output_name_cut = len(input_file) - len(output_extension)
    output_name = input_file[0:output_name_cut] + '_conv_' + str(count) + output_extension

    docker_in_path = '/usr/src/app/_in/'
    docker_out_path = '/usr/src/app/_out/'

    input_argument = docker_in_path + input_file
    output_argument = docker_out_path + output_name
        
    #docker command to mount specified volume
    docker_vol_par = {input_path:{'bind':docker_in_path, 'mode':'rw'}, 
                      output_path:{'bind':docker_out_path, 'mode':'rw'}}

    print ('input argument: ' + input_argument)
    print ('output argument: ' + output_argument)
        
    tool = 'usd_from_gltf '
    command = tool + input_argument + ' ' + output_argument

    #run the defined conversion command in the docker container
    client.containers.run('conv-tools:latest', command, remove=True, volumes=docker_vol_par)
    print('Docker conversion completed!', chr(10))
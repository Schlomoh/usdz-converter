import os
from re import S
import docker
from glob import glob

from utils.path_operations import get_absolute_path, change_extension, new_file_path, is_gltf


def list_files(path: str, recursive: bool) -> 'list[str]':
    """Creates a list of gltf files depending on the input path.

    Args:
        path (str): Input file or directory path
        recursive (bool): If to read out subdirectories

    Returns:
        list[str]: All gltf input files to be converted
    """
    files = []
    if os.path.isfile(path):
        files = [path]
    else:
        if recursive:
            path = os.path.join(path, '**')
        files = glob(path, recursive=recursive)
    return files


class Docker_util:
    """Gets the xrutils docker image and runs the usd_from_gltf tool on the defined
    input files. It processes the input path as either a single file or reads out all 
    eligible files inside a directory and even its subdirectories.

     Args:
            input (string): Path to input file or directory
            output(string): Path to the output directory
            recursive(boolean): If subdirectories of an input path should also be read out.
    """

    docker_base_in = '/usr/src/app/_in/'
    docker_base_out = '/usr/src/app/_out/'
    image_name = 'plattar/python-xrutils'
    image_release = 'release-1.108.3'
    image_full_name = f'{image_name}:{image_release}'

    def __init__(self, input, output, recursive=False):
        self.input = input
        self.output = output
        self.recursive = recursive
        self.instance = docker.from_env()

    def get_image(self):
        """Gets the docker image or pulls it from the hub if not present.

        Returns:
            Model | any: Docker image
        """
        image_list = self.instance.images.list(self.image_full_name)
        if len(image_list) == 0:
            self.instance.images.pull(self.image_name, tag=self.image_release)
        return self.instance.images.get(self.image_full_name)

    def bind_volume(self):
        """Create the binding of directories. Input and output are made available
        inside the docker container.

        Runs the docker container in the detached mode with the tty flag to keep 
        it running.
        """

        absolute_in = get_absolute_path(self.input)
        absolute_out = get_absolute_path(self.output)

        bind_obj = {
            absolute_in: {'bind': self.docker_base_in, 'mode': 'rw'},
            absolute_out: {'bind': self.docker_base_out, 'mode': 'rw'}
        }

        self.container = self.instance.containers.run(
            self.image_full_name, detach=True, volumes=bind_obj, tty=True)

    def call_converter(self, file: str):
        """Runs the command to start the usd_from_gltf tool inside the already
        running container.

        Args:
            file (string): Input gltf file to be converted
        """

        def create_args(f: str):
            """Creates a dictionary containing the input and output path to be placed
            as arguments in the "usd_from_gltf" docker command

            Args:
                f (string): Gltf input file

            Returns:
                dict("inp", "out"): Input and output path
            """
            inp = new_file_path(self.docker_base_in, f)
            out = new_file_path(self.docker_base_out,
                                change_extension(f, '.usdz'))
            return {'inp': inp, 'out': out}

        args = create_args(file)
        cmd = f'usd_from_gltf {args["inp"]} {args["out"]}'
        self.container.exec_run(cmd)

    def stop(self):
        """Stops the container and removes all volumes"""

        self.container.kill()
        self.container.remove(v=True)

    def start(self):
        """Gets the docker image, starts the container with bound volumes,
        reads out input files and then converts all files into the output directory.
        """

        self.get_image()
        self.bind_volume()
        files = list_files(self.input, self.recursive)

        try:
            for file in files:
                if is_gltf(file):
                    print(f'\nConverting {file}... \n')
                    self.call_converter(file)
        except:
            print('Something went wrong while converting.')
            self.stop()
            raise

        self.stop()
        print('Successfully finished converting files!')

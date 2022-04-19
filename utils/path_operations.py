import os


def get_absolute_path(path):
    return os.path.abspath(os.path.dirname(path))


def get_base(path):
    return os.path.basename(path)


def change_extension(file, new_extension):
    return os.path.splitext(file)[0] + new_extension


def new_file_path(new_path, file):
    return os.path.join(new_path, get_base(file))


def check_io(args):
    input, output = args.input, args.output
    exists = os.path.exists

    if not exists(input):
        raise FileNotFoundError(f'The input {input} was not found.')
    elif not exists(output):
        os.mkdir(get_absolute_path(output))

    return input, output


def is_gltf(file):
    extension = os.path.splitext(file)[1]
    for ext in ['.gltf', '.glb']:
        if ext == extension:
            return True
        else:
            return False

import argparse
from termios import INPCK

from utils.path_operations import check_io
from utils.docker_util import Docker_util

DEFAULT_INP = './_in/'
DEFAULT_OUT = './_out/'


def main():
    parser = argparse.ArgumentParser(add_help=True)

    parser.add_argument('input', type=str, default=DEFAULT_INP)
    parser.add_argument('-o', '--output', type=str, default=DEFAULT_OUT)
    parser.add_argument('-r', '--read_dir_recursive', type=bool, default=True)

    arguments = parser.parse_args()

    recursive = arguments.read_dir_recursive
    input, output = check_io(arguments)

    Converter = Docker_util(input, output, recursive)
    Converter.start()


if __name__ == '__main__':
    main()

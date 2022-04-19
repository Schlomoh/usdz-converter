import os
import sys
import tempfile
import time
import argparse

sys.path.append('.')

from modules.Convert import Convert
from modules.Util import Util



class Start:

    def __init__(
                self,
                input_selection,
                output_selection,
                output_format,
                output_name_pattern = None,
                texture_resizing = False,
                resizing_amount = 50,
                texture_quality = 50
                ):
        
        self.arguments = {
            'input_selection' : input_selection,
            'output_selection' : output_selection,
            'output_format' : output_format,
            'output_name' : output_name_pattern,
            'texture_resizing' : texture_resizing,
            'resizing_amount' : resizing_amount,
            'texture_quality' : texture_quality
        }


    def start(self, info = False):
        
        arguments = self.arguments
        start_time = time.time()

        Utility = Util(arguments)
        print('Converter and utility initiation complete...', chr(10))

        selections = Utility.selection_check(
                                            arguments['input_selection'],
                                            arguments['output_selection']
        )

        input_files = selections['input']
        output_path = selections['output']

        arguments['output_path'] = output_path


        Converter = Convert(arguments)

        file_counter = 1
        for single_file in input_files:
            print('Converting input file #' + str(file_counter) + ' of ' + str(len(input_files)))
            with tempfile.TemporaryDirectory() as temp_directory:
                Converter.start(single_file, temp_directory, file_counter)
                file_counter += 1
        
        
       #conversion stats 
        stop_time = time.time()
        
        run_time_sec = round(stop_time - start_time, 2)
        stats = {
                'run_time_sec' : run_time_sec,
               #'file_size' : file_size
                }
        print(stats['run_time_sec'])


def main():
    parser = argparse.ArgumentParser(add_help=True)

    parser.add_argument('input', type=str, help='Single input file or path to directory')
    parser.add_argument('output', type=str, help='Path to output directory')
    parser.add_argument('output_format', type=str, help='Format of ouput file/filess')

    parser.add_argument('-n', '--output_name', type=str, help='Set a certain name for all converted files. The converter adds numeration')
    parser.add_argument('-r', '--resizing', action='store_true', help='Set to activate resizing textures')
    parser.add_argument('-s', '--resizing_amount', type=int, help='Percentage by which to resize textures')
    parser.add_argument('-q', '--texture_quality', type=int, help='Percentage of image texture compression quality')
    
    arguments = parser.parse_args()
    print(chr(10))
    print('Input argument: ' + arguments.input)
    print('Output argument: ' + arguments.output)
    print('Converting to: ' + arguments.output_format.upper(), chr(10))

    if arguments.output_name:
        print('New files will be saved as ' + arguments.output_name + ' and are added a increasing number')

    arguments = {
                'input_argument' : arguments.input,
                'output_argument' : arguments.output,
                'output_format' : arguments.output_format,
                'output_name' : arguments.output_name,
                'texture_resizing' : arguments.resizing,
                'resizing_amount' : arguments.resizing_amount,
                'texture_quality' : arguments.texture_quality
                }    
    convert = Start(
                    arguments['input_argument'],
                    arguments['output_argument'],
                    arguments['output_format'],
                    arguments['output_name'],
                    arguments['texture_resizing'],
                    arguments['resizing_amount'],
                    arguments['texture_quality'])

    convert.start()


if __name__ == "__main__":
    main()


#use sys arg handling through utils class
#complete modulization of utils
#input check on input argument AND output argument (in case of file name in output)
#if output filename given : set output pattern accordingly
#single argument parsing by creating argument dictionaries
#conversion selection through if statement
#docker initiation
#file size compare
#duplicate file check
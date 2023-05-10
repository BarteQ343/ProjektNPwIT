import argparse
import string

parser = argparse.ArgumentParser(description='Konwersja plików XML, JSON i YAML.')

parser.add_argument('input_file', type=str, help='Nazwa pliku wejściowego.')
parser.add_argument('output_file', type=str, help='Nazwa pliku wyjściowego.')
parser.add_argument('format', type=str, help='Format pliku')

args = parser.parse_args()

input_file_extension = args.input_file.split('.')[-1]
input_file_extension = input_file_extension.lower()










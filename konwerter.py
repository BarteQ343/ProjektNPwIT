import argparse
import json

parser = argparse.ArgumentParser(description='Konwersja plików XML, JSON i YAML.')

parser.add_argument('input_file', type=str, help='Nazwa pliku wejściowego.')
parser.add_argument('output_file', type=str, help='Nazwa pliku wyjściowego.')

args = parser.parse_args()

input_file_extension = args.input_file.split('.')[-1]
input_file_extension = input_file_extension.lower()

output_file_extension = args.output_file.split('.')[-1]
output_file_extension = output_file_extension.lower()

# wczytywanie danych

if input_file_extension == 'json':
    with open(args.input_file, 'r') as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError as e:
            print('Niepoprawny format pliku.', str(e))
            exit(1)


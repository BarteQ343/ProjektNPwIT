import argparse
import json
import yaml

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

if input_file_extension == 'yaml':
    with open(args.input_file, 'r') as file:
        try:
            data = yaml.safe_load(file)
        except yaml.YAMLError as e:
            print('Niepoprawny format pliku YAML.', str(e))
            exit(1)


# Funkcje zapisywania danych do nowego formatu


def same_extension():
    print("Format pliku wejściowego i wyjściowego jest taki sam! Plik niie został utworzony.")
    exit(1)



def json_to_yaml():
    with open(args.output_file, 'w') as file:
        yaml.dump(data, file)


def yaml_to_json():
    with open(args.output_file, 'w') as file:
        json.dump(data, file)


# Wywoływanie funkcji

if input_file_extension == output_file_extension:
    same_extension()


if input_file_extension == 'json':
    if output_file_extension == 'yaml':
        print("Konwertowanie pliku json na yaml...")
        json_to_yaml()

if input_file_extension == 'yaml':
    if output_file_extension == 'json':
        print("Konwertowanie pliku yaml na json...")
        yaml_to_json()


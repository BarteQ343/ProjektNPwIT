import argparse
import json
import yaml
import os
import xmltodict

parser = argparse.ArgumentParser(description='Konwersja plików XML, JSON i YAML.')

parser.add_argument('input_file', type=str, help='Nazwa pliku wejściowego.')
parser.add_argument('output_file', type=str, help='Nazwa pliku wyjściowego.')
args = parser.parse_args()

if not os.path.isfile(args.input_file):
    print(f"Plik wejściowy '{args.input_file}' nie istnieje.")
    exit(1)

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

elif input_file_extension == 'yaml':
    with open(args.input_file, 'r') as file:
        try:
            data = yaml.safe_load(file)

        except Exception as e:
            print(f'Błąd odczytu pliku XML: {e}')
            exit(1)

elif input_file_extension == 'xml':
    try:
        with open(args.input_file) as xml_file:
            data = xmltodict.parse(xml_file.read())
    except xmltodict.ExpatError as e:
        print('Niepoprawny format pliku XML.', str(e))
        exit(1)
else:
    print('Niepoprawny format pliku wejściowego. Dostępne formaty: xml, json, yaml.')
    exit(1)

# Funkcje zapisywania danych do nowego formatu
def same_extension():
    print("Format pliku wejściowego i wyjściowego jest taki sam! Plik nie został utworzony.")
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
        yaml.dump(data, file, indent=4)

def yaml_to_json():
    with open(args.output_file, 'w') as file:
        json.dump(data, file, indent=4)


def json_to_xml():
    xml_file = open(args.output_file, "w")
    xmltodict.unparse(data, output=xml_file, pretty=True)
    xml_file.close()

def yaml_to_xml():
    xml_file = open(args.output_file, "w")
    xmltodict.unparse(data, output=xml_file, pretty=True)
    xml_file.close()

def xml_to_json():
    json_data = json.dumps(data, indent=4)

    with open(args.output_file, "w") as json_file:
        json_file.write(json_data)
        json_file.close()

def xml_to_yaml():
    yaml_data = yaml.dump(data, indent=4)

    with open(args.output_file, "w") as yaml_file:
        yaml_file.write(yaml_data)
        yaml_file.close()

# Wywoływanie funkcji

if input_file_extension == output_file_extension:
    same_extension()


elif input_file_extension == 'json':
    if output_file_extension == 'yaml':
        print("Konwertowanie pliku json na yaml...")
        json_to_yaml()

    elif output_file_extension == 'xml':
        print("Konwertowanie pliku json na xml...")
        json_to_xml()


elif input_file_extension == 'yaml':
    if output_file_extension == 'json':
        print("Konwertowanie pliku yaml na json...")
        yaml_to_json()

    elif output_file_extension == 'xml':
        print("Konwertowanie pliku yaml na xml...")
        yaml_to_xml()

elif input_file_extension == 'xml':
    if output_file_extension == 'json':
        print("Konwertowanie pliku xml na json...")
        xml_to_json()

    elif output_file_extension == 'yaml':
        print("Konwertowanie pliku xml na yaml...")
        xml_to_yaml()

else:
    print("Nieobsługiwana kombinacja formatów plików.")

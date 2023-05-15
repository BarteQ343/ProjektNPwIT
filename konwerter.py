import argparse
import json
import yaml
import xml.etree.ElementTree as ET
import os

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
        except yaml.YAMLError as e:
            print('Niepoprawny format pliku YAML.', str(e))
            exit(1)

elif input_file_extension == 'xml':
    try:
        data = ET.parse(args.input_file).getroot()
    except ET.ParseError as e:
        print('Niepoprawny format pliku XML.', str(e))
        exit(1)
else:
    print('Niepoprawny format pliku wejściowego. Dostępne formaty: xml, json, yaml.')
    exit(1)

# Funkcje zapisywania danych do nowego formatu
def same_extension():
    print("Format pliku wejściowego i wyjściowego jest taki sam! Plik nie został utworzony.")
    exit(1)

def json_to_yaml():
    with open(args.output_file, 'w') as file:
        yaml.dump(data, file)

def yaml_to_json():
    with open(args.output_file, 'w') as file:
        json.dump(data, file)

def json_to_xml():
    root = ET.Element('root')
    for key in data:
        node = ET.SubElement(root, key)
        node.text = str(data[key])
    tree = ET.ElementTree(root)
    tree.write(args.output_file, encoding='UTF-8', xml_declaration=True)

def yaml_to_xml():
    root = ET.Element('root')
    for key, value in data.items():
        node = ET.SubElement(root, key)
        if isinstance(value, dict):
            for subkey, subvalue in value.items():
                subnode = ET.SubElement(node, subkey)
                subnode.text = str(subvalue)
        else:
            node.text = str(value)
    tree = ET.ElementTree(root)
    tree.write(args.output_file, encoding='UTF-8', xml_declaration=True)

def xml_to_json():
    data_dict = {}
    for elem in data:
        if list(elem):
            data_dict[elem.tag] = elem.attrib
            for subelem in elem:
                data_dict[elem.tag][subelem.tag] = subelem.text
        elif elem.text:
            data_dict[elem.tag] = elem.text
    with open(args.output_file, 'w') as file:
        json.dump(data_dict, file)

def xml_to_yaml():
    data_dict = {}
    for elem in data:
        if list(elem):
            elem_dict = {}
            for subelem in elem:
                elem_dict[subelem.tag] = subelem.text
            data_dict[elem.tag] = elem_dict
        elif elem.text:
            data_dict[elem.tag] = elem.text
    with open(args.output_file, 'w') as file:
        yaml.dump(data_dict, file)

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
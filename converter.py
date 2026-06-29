import sys
import os
import json
import yaml
import xml.etree.ElementTree as ET

def load_json(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"Błąd składni JSON w pliku {path}: {e}")
        sys.exit(1)

def save_json(data, path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def load_yaml(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except yaml.YAMLError as e:
        print(f"Błąd składni YAML w pliku {path}: {e}")
        sys.exit(1)

def save_yaml(data, path):
    with open(path, 'w', encoding='utf-8') as f:
        yaml.safe_dump(data, f, default_flow_style=False, allow_unicode=True)

def xml_to_dict(element):
    if len(element) == 0:
        return element.text
    return {child.tag: xml_to_dict(child) for child in element}

def dict_to_xml(element, data):
    if isinstance(data, dict):
        for key, value in data.items():
            child = ET.SubElement(element, key)
            dict_to_xml(child, value)
    else:
        element.text = str(data)

def load_xml(path):
    try:
        tree = ET.parse(path)
        return xml_to_dict(tree.getroot())
    except ET.ParseError as e:
        print(f"Błąd składni XML w pliku {path}: {e}")
        sys.exit(1)

def save_xml(data, path):
    root = ET.Element("root")
    dict_to_xml(root, data)
    tree = ET.ElementTree(root)
    ET.indent(tree, space="    ")
    tree.write(path, encoding='utf-8', xml_declaration=True)

def main():
    if len(sys.argv) != 3:
        print("Sposób użycia: python converter.py pathFile1.x pathFile2.y")
        sys.exit(1)

    in_file, out_file = sys.argv[1], sys.argv[2]
    
    if not os.path.exists(in_file):
        print(f"Błąd: Plik wejściowy '{in_file}' nie istnieje!")
        sys.exit(1)

    ext_in = os.path.splitext(in_file)[1].lower()
    ext_out = os.path.splitext(out_file)[1].lower()

    if ext_in == '.json': data = load_json(in_file)
    elif ext_in in ['.yml', '.yaml']: data = load_yaml(in_file)
    elif ext_in == '.xml': data = load_xml(in_file)
    else:
        print(f"Błąd: Nieobsługiwany format wejściowy '{ext_in}'!")
        sys.exit(1)

    if ext_out == '.json': save_json(data, out_file)
    elif ext_out in ['.yml', '.yaml']: save_yaml(data, out_file)
    elif ext_out == '.xml': save_xml(data, out_file)
    else:
        print(f"Błąd: Nieobsługiwany format wyjściowy '{ext_out}'!")
        sys.exit(1)

    print(f"Sukces! Przekonwertowano {in_file} do {out_file}")

if __name__ == "__main__":
    main()

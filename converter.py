
import sys

import os

import json

import yaml

import xml.etree.ElementTree as ET

import threading

import tkinter as tk

from tkinter import filedialog, messagebox



def load_json(path):

    try:

        with open(path, 'r', encoding='utf-8') as f:

            return json.load(f)

    except json.JSONDecodeError as e:

        raise ValueError(f"Błąd składni JSON: {e}")



def save_json(data, path):

    with open(path, 'w', encoding='utf-8') as f:

        json.dump(data, f, indent=4, ensure_ascii=False)



def load_yaml(path):

    try:

        with open(path, 'r', encoding='utf-8') as f:

            return yaml.safe_load(f)

    except yaml.YAMLError as e:

        raise ValueError(f"Błąd składni YAML: {e}")



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

        raise ValueError(f"Błąd składni XML: {e}")



def save_xml(data, path):

    root = ET.Element("root")

    dict_to_xml(root, data)

    tree = ET.ElementTree(root)

    ET.indent(tree, space="    ")

    tree.write(path, encoding='utf-8', xml_declaration=True)



def async_convert(in_file, out_file, callback_success, callback_error):

    def worker():

        try:

            if not os.path.exists(in_file):

                raise FileNotFoundError(f"Plik wejściowy '{in_file}' nie istnieje!")



            ext_in = os.path.splitext(in_file)[1].lower()

            ext_out = os.path.splitext(out_file)[1].lower()



            if ext_in == '.json': data = load_json(in_file)

            elif ext_in in ['.yml', '.yaml']: data = load_yaml(in_file)

            elif ext_in == '.xml': data = load_xml(in_file)

            else: raise ValueError(f"Nieobsługiwany format wejściowy '{ext_in}'!")



            if ext_out == '.json': save_json(data, out_file)

            elif ext_out in ['.yml', '.yaml']: save_yaml(data, out_file)

            elif ext_out == '.xml': save_xml(data, out_file)

            else: raise ValueError(f"Nieobsługiwany format wyjściowy '{ext_out}'!")



            callback_success()

        except Exception as e:

            callback_error(str(e))



    threading.Thread(target=worker, daemon=True).start()



class ConverterApp:

    def __init__(self, root):

        self.root = root

        self.root.title("Konwerter plików - JSON, YAML, XML")

        self.root.geometry("500x250")

        self.root.resizable(False, False)



        tk.Label(root, text="Plik źródłowy:").pack(anchor="w", px=20, py=(15, 2))

        self.frame_in = tk.Frame(root)

        self.frame_in.pack(fill="x", px=20)

        self.entry_in = tk.Entry(self.frame_in)

        self.entry_in.pack(side="left", fill="x", expand=True, ipy=4)

        tk.Button(self.frame_in, text="Przeglądaj...", command=self.select_input).pack(side="right", px=(5, 0))



        tk.Label(root, text="Plik docelowy:").pack(anchor="w", px=20, py=(10, 2))

        self.frame_out = tk.Frame(root)

        self.frame_out.pack(fill="x", px=20)

        self.entry_out = tk.Entry(self.frame_out)

        self.entry_out.pack(side="left", fill="x", expand=True, ipy=4)

        tk.Button(self.frame_out, text="Zapisz jako...", command=self.select_output).pack(side="right", px=(5, 0))



        self.lbl_status = tk.Label(root, text="Status: Oczekiwanie na pliki", fg="gray")

        self.lbl_status.pack(py=15)



        self.btn_convert = tk.Button(root, text="Konwertuj asynchronicznie", bg="#238636", fg="white", font=("Arial", 10, "bold"), command=self.start_conversion)

        self.btn_convert.pack(fill="x", px=20, ipy=6)



    def select_input(self):

        file_path = filedialog.askopenfilename(filetypes=[("Obsługiwane pliki", "*.json;*.yaml;*.yml;*.xml")])

        if file_path:

            self.entry_in.delete(0, tk.END)

            self.entry_in.insert(0, file_path)



    def select_output(self):

        file_path = filedialog.asksaveasfilename(filetypes=[("JSON", "*.json"), ("YAML", "*.yaml"), ("XML", "*.xml")])

        if file_path:

            self.entry_out.delete(0, tk.END)

            self.entry_out.insert(0, file_path)



    def start_conversion(self):

        in_p = self.entry_in.get().strip()

        out_p = self.entry_out.get().strip()



        if not in_p or not out_p:

            messagebox.showwarning("Błąd", "Musisz wybrać oba pliki!")

            return



        self.btn_convert.config(state="disabled", text="Przetwarzanie...")

        self.lbl_status.config(text="Trwa konwersja danych w tle...", fg="blue")



        def on_success():

            self.root.after(0, lambda: [

                messagebox.showinfo("Sukces", "Konwersja zakończona powodzeniem!"),

                self.lbl_status.config(text="Sukces! Plik zapisany.", fg="green"),

                self.btn_convert.config(state="normal", text="Konwertuj asynchronicznie")

            ])



        def on_error(msg):

            self.root.after(0, lambda: [

                messagebox.showerror("Błąd", msg),

                self.lbl_status.config(text="Wystąpił błąd podczas pracy.", fg="red"),

                self.btn_convert.config(state="normal", text="Konwertuj asynchronicznie")

            ])



        async_convert(in_p, out_p, on_success, on_error)



def main():

    if len(sys.argv) == 3:

        in_file, out_file = sys.argv[1], sys.argv[2]

        if not os.path.exists(in_file):

            print(f"Błąd: Plik '{in_file}' nie istnieje!")

            sys.exit(1)

        

        ext_in = os.path.splitext(in_file)[1].lower()

        ext_out = os.path.splitext(out_file)[1].lower()



        try:

            if ext_in == '.json': data = load_json(in_file)

            elif ext_in in ['.yml', '.yaml']: data = load_yaml(in_file)

            elif ext_in == '.xml': data = load_xml(in_file)

            else: sys.exit(1)



            if ext_out == '.json': save_json(data, out_file)

            elif ext_out in ['.yml', '.yaml']: save_yaml(data, out_file)

            elif ext_out == '.xml': save_xml(data, out_file)

            else: sys.exit(1)

            print("Sukces!")

        except Exception as e:

            print(f"Błąd: {e}")

            sys.exit(1)

            

    else:

        root = tk.Tk()

        app = ConverterApp(root)

        root.mainloop()if __name__ == "__main__":

    main()


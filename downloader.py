from subject_parser import Parser
from connection import Connection
import os
import sys
import re
from termcolor import colored


class Downloader:
    def __init__(self, connection: Connection, path):
        self.connection = connection
        self._set_path(path)
        self.root = "wis-materials"
        self.url = "https://wis.fit.vutbr.cz/FIT/st/cfs.php.cs?file=/course"
        self.abbreviations = self._get_subject_abbreviations()
        self.count = len(self.abbreviations)
        self.done = 0

    def _set_path(self, path):
        if path is not None:
            try:
                os.chdir(path)
            except FileNotFoundError:
                sys.stderr.write("[ERROR] Path \""+path+"\" not found!")
                sys.exit(1)

    def _get_subject_abbreviations(self):
        content = self.connection.get_contents(self.url)
        parser = Parser(content)
        return parser.get_column_values(3)

    def download(self):
        print(colored("Downloading of "+str(self.count)+" courses...", "cyan"))
        print("-----------------------------------------------------------")
        if os.path.exists(self.root) and os.path.isdir(self.root):
            os.system("rm -r "+self.root)
        os.system("mkdir "+self.root)
        for abbrev in self.abbreviations:
            content = self.connection.get_contents(self.url+"/"+abbrev)
            os.system("mkdir "+self.root+"/"+abbrev)
            self._process_subject(content, abbrev)
        print(colored("Downloading of " + str(self.count) + " courses is completed.", "green"))
        print("-----------------------------------------------------------")

    def _get_path(self, url):
        return re.search(r"(?<=course).*", url).group(0)

    def _process_subject(self, content, subject):
        self.done += 1
        print(colored("("+str(self.done)+"/"+str(self.count)+")", "yellow"), colored("Downloading of " + subject + " has started...", "cyan"))
        material_types = Parser(content).get_material_types()
        for material_type in material_types:
            url = self.url+"/"+subject+"/"+material_type
            subject_content = self.connection.get_contents(url)
            self._process_subject_material_type(subject_content, self._get_path(url))
        print(colored("("+str(self.done)+"/"+str(self.count)+")", "yellow"), colored(subject, "cyan"), colored(u'\u2713', "green"))
        print("-----------------------------------------------------------")

    def _process_subject_material_type(self, content, path):
        parser = Parser(content)
        folder_content = parser.get_subject_materials_folder_dictionary()
        if folder_content is None:
            return
        os.system("mkdir " + self.root + path)
        for key, value in folder_content.items():
            if value == "yes":
                new_page_content = self.connection.get_contents(self.url+path+"/"+key)
                new_url = self._get_path(self.url+path+"/"+key)
                self._process_subject_material_type(new_page_content, new_url)
            else:
                file_path = self.root+(self._get_path(self.url+path))
                self.connection.download_file(self.url+path+"/"+key, file_path)



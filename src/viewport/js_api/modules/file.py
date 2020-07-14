import os
import json

from typing import Type

# import viewport
from data import pak_tools

from viewport.js_api import JsApi
import viewport




def create_files_module(api: Type[JsApi]):
    def read_json_file(self, filepath):
        file = open(filepath, 'r', encoding='utf-8')
        retVal = json.load(file)
        # print(retVal)
        file.close()
        return retVal

    def write_json_file(self, filepath, contents):
        file = open(filepath, 'w', encoding='utf-8')
        json.dump(contents, file, sort_keys=False, indent=4, ensure_ascii=False)
        file.close()

    def read_file(self, filepath):
        file = open(filepath, 'r')
        retVal = file.read()
        file.close()
        return retVal

    def write_file(self, filepath, contents):
        file = open(filepath, 'w')
        file.write(contents)
        file.close()

    def listdir(self, *args):
        return os.listdir(*args)

    def remove(self, *args):
        return os.remove(*args)

    def link(self, *args):
        return os.link(*args)

    def mkdir(self, *args):
        return os.mkdir(*args)

    def makedirs(self, *args):
        return os.makedirs(*args)

    def getcwd(self, *args):
        return os.getcwd()

    def isfile(self, *args):
        return os.path.isfile(*args)

    def exists(self, *args):
        return os.path.exists(*args)

    def isdir(self, *args):
        return os.path.isdir(*args)


    api.add_module_method_list("files", [
        listdir,
        remove,
        link,
        mkdir,
        makedirs,
        getcwd,
        isfile,
        isdir,
        exists,
        read_file,
        read_json_file,
        write_file,
        write_json_file
    ])


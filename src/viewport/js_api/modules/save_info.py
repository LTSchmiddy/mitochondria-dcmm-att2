import os
import json

from typing import Type

# import viewport
from data import saves

from viewport.js_api import JsApi
import viewport
import mitochondria


def create_saves_module(api: Type[JsApi]):
    def count_current_saves(self):
        return saves.save_man.count_current_save_slots()

    def list_current_saves_found(self):
        return  saves.save_man.list_current_saves_found()

    def load_past_save_file(self, slot, path):
        return saves.save_man.load_past_save_file( slot, path)


    api.add_module_method_list("saves", [
        count_current_saves,
        list_current_saves_found,
        load_past_save_file
    ])


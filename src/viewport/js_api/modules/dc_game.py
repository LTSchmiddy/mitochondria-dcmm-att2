import os
import json

from typing import Type

# import viewport
from data import deadcells_game

from viewport.js_api import JsApi
import viewport
import mitochondria


def create_game_module(api: Type[JsApi]):
    def check_for_game(self):
        return deadcells_game.game_man.look_for_game_proc()

    def start_game(self):
        return deadcells_game.game_man.start_game()

    def quit_game(self):
        return deadcells_game.game_man.quit_game()

    def is_game_detected(self):
        return deadcells_game.game_man.is_game_detected()

    api.add_module_method_list("dc_game", [
        check_for_game,
        start_game,
        quit_game,
        is_game_detected
    ])


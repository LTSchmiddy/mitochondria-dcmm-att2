import os
import sys
import shutil
import ntpath

import psutil


from settings import current, paths

default_process_names = ["deadcells.exe", "deadcells_gl.exe"]

class GameMan:
    game_proc: psutil.Process

    def __init__(self):
        global default_process_names
        self.process_names = default_process_names[:]

        self.game_proc = None


    def is_game_detected(self):
        return self.game_proc is not None and self.game_proc.is_running()


    def start_game(self):
        if self.is_game_detected():
            print("Game is already running.")
            return

        self.game_proc = psutil.Popen(paths.get_game_exec())


    def quit_game(self):
        if not self.is_game_detected():
            print("Game not running.")
            return

        self.game_proc.terminate()


    def update(self):
        if not self.is_game_detected():
            self.look_for_game_proc()



    def look_for_game_proc(self):
        for proc in psutil.process_iter(['pid', 'name', 'username']):
            if proc.name() in self.process_names:
                self.game_proc = proc


game_man = GameMan()
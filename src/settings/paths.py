import settings
# from settings import *
import os

import data.deadcells_game

settings.load_settings()
# General
def get_backups_dir() -> str:
    # global current
    return settings.current['dirs']['operating_dir'] + "/backups"

def get_game_exec() -> str:
    # global current
    return os.path.join(settings.current['dirs']['game_directory'], data.deadcells_game.game_man.process_names[0]).replace("\\", "/")

def get_main_pak() -> str:
    # global current
    return os.path.join(settings.current['dirs']['game_directory'], settings.current['files']['main_pak']).replace("\\", "/")

def get_master_pak() -> str:
    # global current
    # return os.path.join(current['dirs']['game_directory'], current['files']['master_pak'])
    return os.path.join(settings.current['dirs']['operating_dir'], settings.current['files']['master_pak']).replace("\\", "/")


def get_master_backup_pak() -> str:
    # return os.path.join(current['dirs']['game_directory'], get_backups_dir() + "/" + current['files']['master_backup_pak'])
    return os.path.join(get_backups_dir(), settings.current['files']['master_backup_pak']).replace("\\", "/")


def get_main_cdb():
    return get_extract_res_dir() + "/data.cdb"


# Extraction and Packing:
def get_extract_dir() -> str:
    # global current
    return settings.current['dirs']['operating_dir'] + "/" + settings.current['dirs']['extraction_profile']

def get_extract_res_dir() -> str:
    # global current
    return get_extract_dir() + "/res"

def get_extract_cdb_dir():
    # global current
    return get_extract_dir() + "/cdb"


def get_pak_tool() -> str:
    # global current
    return os.path.join(settings.current['dirs']['game_directory'], settings.current['dirs']['tools_dir'] + "/PAKTool.exe").replace("\\", "/")

def get_cdb_tool() -> str:
    # global current
    return os.path.join(settings.current['dirs']['game_directory'], settings.current['dirs']['tools_dir'] + "/CDBTool.exe").replace("\\", "/")

# Saves:

def get_save_backup_dir():
    return os.path.join(settings.current['dirs']['operating_dir'], settings.current['dirs']['saves_backup_dir']).replace("\\", "/")

def get_save_slot_backup_dir(slot: int):
    return get_save_backup_dir() + f"/{slot}"

def get_game_save_dir():
    return os.path.join(settings.current['dirs']['game_directory'], settings.current['dirs']['game_save_dir']).replace("\\", "/")

def get_game_save_slot_path(slot: int):
    return os.path.join(get_game_save_dir(), f"user_{slot}.dat").replace("\\", "/")
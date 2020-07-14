import sys
import time
import os
import shutil
import hashlib

from data import std_handler
std_handler.init()

import settings
import settings.paths
from data.pak_tools import tool_man
import webview as wv
import interface_flask
import viewport
import data.saves


def run_startup(window: wv.window):
    window.load_url(interface_flask.get_startup_addr())

    while True:
        v_result = settings.validate_settings()

        if len(v_result) != 0:
            window.load_url(interface_flask.get_launch_settings_addr())
        else:
            break

        while window.get_current_url() != interface_flask.get_startup_addr():
            pass


    print(window.get_current_url())

    while not window.get_current_url() == interface_flask.get_startup_addr():
        print("waiting")
        time.sleep(.5)

    # time.sleep(5)

    validate_mainpak_checksum()
    generate_operating_dirs()




def validate_mainpak_checksum():
    if settings.current['files']['main_pak_checksum'] == "":
        print("Checksum never generated. Generating now...")
        tool_man.update_main_pak_checksum()
        return

    print("Validating main.pak checksum...")

    if settings.current['files']['main_pak_checksum'] != tool_man.get_main_pak_checksum():
        print("WARNING: main.pak seems to have been modified externally. Prompting for resolution...")
        message = "WARNING: main.pak seems to have been modified externally. It is possible that Dead Cells has been updated." \
                  "Do you want to replace your 'res_master.pak' with this new file? (Not doing so could result in problems)."
        response = viewport.confirm_prompt(message)
        print(response)
        if response:
            generate_master_pak()
            tool_man.update_main_pak_checksum()




# Sub-Methods:
def mkdir_if_missing(dir_path: str):
    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)


def generate_master_pak():
    print(f"Creating '{settings.paths.get_master_pak()}'...")
    shutil.copy(
        settings.paths.get_main_pak(), settings.paths.get_master_pak()
    )

    print(f"Creating '{settings.paths.get_master_backup_pak()}'...")
    shutil.copy(
        settings.paths.get_main_pak(),
        settings.paths.get_master_backup_pak(),
    )

def generate_operating_dirs():
    print("Running startup")
    mkdir_if_missing(settings.current["dirs"]["operating_dir"])
    mkdir_if_missing(settings.paths.get_extract_dir())
    mkdir_if_missing(settings.paths.get_backups_dir())

    mkdir_if_missing(settings.paths.get_save_backup_dir())
    for i in range(0, data.saves.default_num_save_slots):
        mkdir_if_missing(settings.paths.get_save_slot_backup_dir(i))


    # Pak Dirs
    if not os.path.isfile(settings.paths.get_master_pak()):
        print(f"File {settings.paths.get_master_pak()} not present.")

        if not os.path.isfile(settings.paths.get_master_backup_pak()):
            print(
                f"{settings.paths.get_master_backup_pak()} not found either. Assuming that this is a clean installation."
            )
            print(
                "If this is the first time you've run Mitochondria for this Dead Cells installation, this is normal."
            )
            print("If not, then something has gone horribly wrong.")
            print("Anyway, I'll generate these files now. This might take a moment.")

            generate_master_pak()

        else:
            print("Looks like it SOMEHOW got deleted. I'll restore it from the backup.")

            print(f"Creating '{settings.paths.get_master_pak()}'...")
            shutil.copy(
                settings.paths.get_master_backup_pak(), settings.paths.get_master_pak()
            )
        print("Startup Done")



